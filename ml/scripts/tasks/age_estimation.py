# ml/scripts/tasks/age_estimation.py

from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks
import numpy as np
import pandas as pd

def compute_i3m(annotation_df: pd.DataFrame) -> pd.Series:
    """
    Compute the I3M index: sum of inner root distances / tooth length.
    Expects columns: ['root1_x1','root1_y1','root1_x2','root1_y2',
                      'root2_x1','root2_y1','root2_x2','root2_y2',
                      'crown_x1','crown_y1','crown_x2','crown_y2']
    """
    def dist(x1,y1,x2,y2): return np.hypot(x2-x1, y2-y1)
    sums = (
        dist(*annotation_df[['root1_x1','root1_y1','root1_x2','root1_y2']].values.T) +
        dist(*annotation_df[['root2_x1','root2_y1','root2_x2','root2_y2']].values.T)
    )
    length = dist(*annotation_df[['crown_x1','crown_y1','crown_x2','crown_y2']].values.T)
    return sums / length

def build_age_model(input_shape):
    inputs = layers.Input(shape=(*input_shape, 3))
    x = layers.Rescaling(1./255)(inputs)
    x = layers.Conv2D(32,3,activation='relu')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64,3,activation='relu')(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(64,activation='relu')(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)  # binary: minor vs adult
    model = models.Model(inputs, outputs)
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    return model

def train(data_dir: Path, output_dir: Path, img_size: tuple, batch_size: int, epochs: int):
    # Load annotations
    ann = pd.read_csv(data_dir/'annotations.csv')
    i3m = compute_i3m(ann)
    labels = (i3m < 0.08).astype(int)  # 1 => adult (>=18)

    # Image paths & labels
    img_paths = [data_dir/'images'/f for f in ann['filename']]
    ds = tf.data.Dataset.from_tensor_slices((img_paths, labels))
    
    def _load(path, label):
        img = tf.io.read_file(str(path))
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.resize(img, img_size)
        return img, label

    ds = ds.map(_load).batch(batch_size).cache().prefetch(tf.data.AUTOTUNE)

    # Split train/val
    val_size = int(0.2 * len(img_paths))
    val_ds = ds.take(val_size)
    train_ds = ds.skip(val_size)

    # Build & train
    model = build_age_model(img_size)
    chkpt = callbacks.ModelCheckpoint(output_dir/'best_age.h5', save_best_only=True, monitor='val_accuracy')
    es    = callbacks.EarlyStopping(patience=3, monitor='val_loss', restore_best_weights=True)

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[chkpt, es]
    )
    model.save(output_dir/'age_model')
    return history
