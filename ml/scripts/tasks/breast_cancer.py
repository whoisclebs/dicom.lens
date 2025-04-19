# ml/scripts/tasks/breast_cancer.py
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from scripts.train import parse_args

def build_model(img_size):
    inputs = layers.Input(shape=(*img_size, 3))
    x = layers.Rescaling(1./255)(inputs)
    x = layers.Conv2D(32, 3, activation='relu')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(64, activation='relu')(x)
    outputs = layers.Dense(1, activation='sigmoid')(x)
    model = models.Model(inputs, outputs)
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    return model

def train(data_dir: Path, output_dir: Path, img_size: tuple, batch_size: int, epochs: int):
    # Load datasets
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir / 'train',
        labels='inferred',
        label_mode='binary',
        image_size=img_size,
        batch_size=batch_size,
        shuffle=True
    ).cache().prefetch(tf.data.AUTOTUNE)

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir / 'validation',
        labels='inferred',
        label_mode='binary',
        image_size=img_size,
        batch_size=batch_size,
        shuffle=False
    ).cache().prefetch(tf.data.AUTOTUNE)

    # Build and train
    model = build_model(img_size)
    checkpoint = callbacks.ModelCheckpoint(output_dir / 'best_model.h5', monitor='val_accuracy', save_best_only=True)
    earlystop = callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[checkpoint, earlystop]
    )

    # Save final model
    model.save(output_dir)
    return history
