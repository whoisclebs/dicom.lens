#!/usr/bin/env python3

import argparse
from pathlib import Path

import tensorflow as tf
from tensorflow.keras import layers, models, callbacks

def parse_args():
    parser = argparse.ArgumentParser(
        description="Train an image classification model for binary prediction."
    )
    parser.add_argument(
        "--data-dir", required=True,
        help="Base directory with 'train' and 'validation' subfolders."
    )
    parser.add_argument(
        "--output", default="saved_model",
        help="Directory to save the trained model."
    )
    parser.add_argument(
        "--img-size", nargs=2, type=int, default=[224, 224],
        help="Image dimensions (height width)."
    )
    parser.add_argument(
        "--batch-size", type=int, default=32,
        help="Batch size for training."
    )
    parser.add_argument(
        "--epochs", type=int, default=20,
        help="Number of training epochs."
    )
    return parser.parse_args()


def load_dataset(directory: Path, img_size: tuple, batch_size: int, shuffle: bool):
    return tf.keras.preprocessing.image_dataset_from_directory(
        directory,
        labels='inferred',
        label_mode='binary',
        image_size=img_size,
        batch_size=batch_size,
        shuffle=shuffle
    )


def build_model(img_size: tuple) -> tf.keras.Model:
    inputs = layers.Input(shape=(*img_size, 3))
    x = layers.RandomFlip('horizontal')(inputs)
    x = layers.RandomRotation(0.1)(x)
    x = layers.RandomZoom(0.2)(x)
    x = layers.Rescaling(1.0 / 255)(x)
    x = layers.Conv2D(32, 3, activation='relu')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(128, 3, activation='relu')(x)
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


def train_model(model: tf.keras.Model,
                train_ds: tf.data.Dataset,
                val_ds: tf.data.Dataset,
                epochs: int,
                output_dir: str) -> callbacks.History:
    checkpoint = callbacks.ModelCheckpoint(
        filepath=Path(output_dir) / 'best_model.h5',
        monitor='val_accuracy',
        save_best_only=True
    )
    early_stop = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=[checkpoint, early_stop]
    )
    model.save(output_dir)
    return history


def main():
    args = parse_args()
    data_dir = Path(args.data_dir)
    img_size = tuple(args.img_size)

    train_ds = load_dataset(
        data_dir / 'train', img_size, args.batch_size, shuffle=True
    ).cache().prefetch(tf.data.AUTOTUNE)

    val_ds = load_dataset(
        data_dir / 'validation', img_size, args.batch_size, shuffle=False
    ).cache().prefetch(tf.data.AUTOTUNE)

    model = build_model(img_size)
    print(model.summary())

    history = train_model(
        model, train_ds, val_ds, args.epochs, args.output
    )

    # Optionally print final metrics
    val_loss, val_acc, val_auc = model.evaluate(val_ds)
    print(f"Validation - Loss: {val_loss:.4f}, "
          f"Accuracy: {val_acc:.4f}, AUC: {val_auc:.4f}")


if __name__ == "__main__":
    main()