import os
import pathlib
import numpy as np
import torch

from models import AttentionUNet, UNet

DEVICE = "cuda"


def normalize(data: np.ndarray, lower_bound: int, upper_bound: int) -> np.ndarray:
    data = (data - lower_bound) / (upper_bound - lower_bound)
    data[data > 1] = 1
    data[data < 0] = 0
    return data


def main():
    pass


if __name__ == '__main__':
    main()