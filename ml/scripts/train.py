#!/usr/bin/env python3
"""
Unified training CLI for DicomLens tasks.
"""
import argparse
import importlib
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        description="Train a DicomLens task (e.g., breast_cancer, age_estimation, lung_nodule)"
    )
    subparsers = parser.add_subparsers(dest="task", required=True)

    common = {
        "data_dir": {
            "flags": ["--data-dir"],
            "kwargs": {"type": Path, "required": True, "help": "Path to task-specific dataset root"}
        },
        "output_dir": {
            "flags": ["--output-dir"],
            "kwargs": {"type": Path, "required": True, "help": "Directory to save trained model"}
        },
        "img_size": {
            "flags": ["--img-size"],
            "kwargs": {"nargs": 2, "type": int, "default": [224, 224], "help": "Image size H W"}
        },
        "batch_size": {
            "flags": ["--batch-size"],
            "kwargs": {"type": int, "default": 32, "help": "Training batch size"}
        },
        "epochs": {
            "flags": ["--epochs"],
            "kwargs": {"type": int, "default": 20, "help": "Number of epochs"}
        }
    }

    # Define supported tasks
    tasks = ["breast_cancer"]
    for t in tasks:
        sp = subparsers.add_parser(t, help=f"Train the {t.replace('_', ' ')} model")
        for arg, opts in common.items():
            sp.add_argument(*opts["flags"], dest=arg, **opts["kwargs"])

    return parser.parse_args()


def main():
    args = parse_args()
    # Dynamically import the selected task module
    module_path = f"scripts.tasks.{args.task}"
    task_module = importlib.import_module(module_path)

    # Convert img_size list to tuple
    img_size = tuple(args.img_size)

    # Call the train function in the task module
    task_module.train(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        img_size=img_size,
        batch_size=args.batch_size,
        epochs=args.epochs
    )


if __name__ == "__main__":
    main()
