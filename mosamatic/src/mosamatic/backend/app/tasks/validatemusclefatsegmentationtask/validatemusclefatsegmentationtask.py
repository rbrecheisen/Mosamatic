import os
import pandas as pd

from ...utils import (
    load_dicom, 
    get_pixels_from_tag_file, 
    load_numpy_array, 
    calculate_dice_score,
    MUSCLE, VAT, SAT,
)
from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()


class ValidateMuscleFatSegmentationTask(Task):
    def find_pred_mask_file(self, true_mask_file, pred_mask_files):
        true_mask_file_name = os.path.split(true_mask_file)[1][:-4]
        root_path = os.path.split(pred_mask_files[0])[0]
        pred_mask_file_name = true_mask_file_name + '.dcm.seg.npy'
        pred_mask_file = os.path.join(root_path, pred_mask_file_name)
        return pred_mask_file
    
    def execute(self):
        true_mask_files = self.input('true_mask_files')
        pred_mask_files = self.input('pred_mask_files')
        nr_steps = len(true_mask_files)
        data = {
            'dice_muscle': [],
            'dice_vat': [],
            'dice_sat': [],
        }
        for step in range(nr_steps):
            if self.is_canceled():
                break
            true_mask_file = true_mask_files[step]
            if true_mask_file.endswith('.tag'):
                pred_mask_file = self.find_pred_mask_file(true_mask_file, pred_mask_files)
                if pred_mask_file:
                    true_mask = get_pixels_from_tag_file(true_mask_file)
                    true_mask = true_mask.reshape((512, 512))
                    pred_mask = load_numpy_array(pred_mask_file)
                    dice_muscle, dice_vat, dice_sat = (
                        calculate_dice_score(true_mask, pred_mask, MUSCLE),
                        calculate_dice_score(true_mask, pred_mask, VAT),
                        calculate_dice_score(true_mask, pred_mask, SAT),
                    )
                    data['dice_muscle'].append(dice_muscle)
                    data['dice_vat'].append(dice_vat)
                    data['dice_sat'].append(dice_sat)
            self.set_progress(step, nr_steps)
        df = pd.DataFrame(data=data)
        csv_file_path = os.path.join(self.output('dice_scores'), 'dice_scores.csv')
        df.to_csv(csv_file_path, index=False, sep=';')
