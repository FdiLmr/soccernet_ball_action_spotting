import json
import argparse
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from argus.callbacks import (
    MonitorCheckpoint,
    LoggingToFile,
    LoggingToCSV,
    CosineAnnealingLR,
    LambdaLR,
)

from src.ball_action.datasets import TrainActionBallDataset, ValActionBallDataset
from src.ball_action.argus_models import BallActionModel
from src.ball_action.annotations import get_videos_data
from src.ball_action import constants

import cv2
cv2.setNumThreads(0)
cv2.ocl.setUseOpenCL(False)


parser = argparse.ArgumentParser()
parser.add_argument('--experiment', required=True, type=str)
args = parser.parse_args()


def get_lr(base_lr, batch_size):
    return base_lr * (batch_size / 8)


BATCH_SIZE = 4
BASE_LR = 3e-4
FRAME_STACK_SIZE = 15
CONFIG = dict(
    batch_size=BATCH_SIZE,
    base_lr=BASE_LR,
    frame_stack_size=FRAME_STACK_SIZE,
    frame_stack_step=2,
    target_gauss_scale=3.0,
    train_epoch_size=2000,
    num_workers=8,
    num_epochs=[2, 14],
    stages=['warmup', 'train'],
    min_base_lr=BASE_LR * 0.01,
    experiments_dir=str(constants.experiments_dir / args.experiment),
    argus_params={
        'nn_module': ('ActionTimm', {
            "model_name": "tf_efficientnetv2_b0",
            "num_classes": constants.num_classes,
            "num_frames": FRAME_STACK_SIZE,
            "pretrained": True,
        }),
        'loss': 'BCEWithLogitsLoss',
        'optimizer': ('AdamW', {'lr': get_lr(BASE_LR, BATCH_SIZE)}),
        'device': [f'cuda:{i}' for i in range(torch.cuda.device_count())],
    },
)


def train_ball_action(config: dict, save_dir: Path):
    model = BallActionModel(config["argus_params"])
    if 'pretrained' in model.params['nn_module'][1]:
        model.params['nn_module'][1]['pretrained'] = False

    for num_epochs, stage in zip(config["num_epochs"], config["stages"]):
        train_data = get_videos_data(constants.train_games)
        train_dataset = TrainActionBallDataset(
            train_data,
            frame_stack_size=config["frame_stack_size"],
            frame_stack_step=config["frame_stack_step"],
            target_gauss_scale=config["target_gauss_scale"],
            epoch_size=config["train_epoch_size"]
        )
        print(f"Train dataset len {len(train_dataset)}")
        val_data = get_videos_data(constants.val_games)
        val_dataset = ValActionBallDataset(
            val_data,
            frame_stack_size=config["frame_stack_size"],
            frame_stack_step=config["frame_stack_step"],
            target_gauss_scale=config["target_gauss_scale"],
        )
        print(f"Val dataset len {len(val_dataset)}")
        train_loader = DataLoader(train_dataset, batch_size=config["batch_size"],
                                  shuffle=True, drop_last=True,
                                  num_workers=config["num_workers"])
        val_loader = DataLoader(val_dataset, batch_size=config["batch_size"] * 2,
                                shuffle=False, num_workers=config["num_workers"])

        callbacks = [
            LoggingToFile(save_dir / 'log.txt', append=True),
            LoggingToCSV(save_dir / 'log.csv', append=True)
        ]

        num_iterations = (len(train_dataset) // config["batch_size"]) * num_epochs
        if stage == 'train':
            callbacks += [
                MonitorCheckpoint(save_dir, monitor='val_loss', max_saves=1),
                CosineAnnealingLR(
                    T_max=num_iterations,
                    eta_min=get_lr(config["min_base_lr"], config["batch_size"]),
                    step_on_iteration=True
                )
            ]
        elif stage == 'warmup':
            callbacks += [
                LambdaLR(lambda x: x / num_iterations,
                         step_on_iteration=True)
            ]

        model.fit(train_loader,
                  val_loader=val_loader,
                  num_epochs=num_epochs,
                  callbacks=callbacks)


if __name__ == "__main__":
    experiments_dir = Path(CONFIG["experiments_dir"])
    print("Experiment dir", experiments_dir)
    if not experiments_dir.exists():
        experiments_dir.mkdir(parents=True, exist_ok=True)
    else:
        print(f"Folder {experiments_dir} already exists.")

    with open(experiments_dir / 'source.py', 'w') as outfile:
        outfile.write(open(__file__).read())

    print("Experiment config", CONFIG)
    with open(experiments_dir / 'config.json', 'w') as outfile:
        json.dump(CONFIG, outfile, indent=4)

    train_ball_action(CONFIG, experiments_dir)