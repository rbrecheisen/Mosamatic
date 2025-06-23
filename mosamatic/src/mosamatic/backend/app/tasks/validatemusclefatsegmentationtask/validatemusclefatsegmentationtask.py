import os
import pandas as pd

from ...utils import load_dicom
from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()


class ValidateMuscleFatSegmentationTask(Task):
    def find_pred_mask_file(self, true_mask_file, pred_mask_files):
        for pred_mask_file in pred_mask_files:
            pred_mask_file_name = os.path.split(pred_mask_file)[1][:-8] # .seg.npy
            true_mask_file_name = os.path.split(true_mask_file)[1][:-4] # .tag
            if pred_mask_file_name == true_mask_file_name:
                return pred_mask_file
        return None
    
    def execute(self):
        true_mask_files = self.input('true_mask_files')
        pred_mask_files = self.input('pred_mask_files')
        nr_steps = len(true_mask_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            true_mask_file = true_mask_files[step]
            pred_mask_file = self.find_pred_mask_file(true_mask_file, pred_mask_files)
            print(pred_mask_file)