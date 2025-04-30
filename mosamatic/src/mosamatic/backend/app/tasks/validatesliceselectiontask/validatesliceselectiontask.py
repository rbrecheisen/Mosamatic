import os
import pandas as pd

from ...utils import load_dicom
from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()


class ValidateSliceSelectionTask(Task):
    def find_manual_file(self, auto_file, manually_selected):
        p_auto = load_dicom(auto_file, stop_before_pixels=True)
        for f in manually_selected:
            p_manual = load_dicom(f, stop_before_pixels=True)
            if p_manual.SeriesInstanceUID == p_auto.SeriesInstanceUID:
                return f
        return None
    
    def compare_z_positions(self, auto_file, manual_file):
        p_auto = load_dicom(auto_file, stop_before_pixels=True)
        z_auto = p_auto.ImagePositionPatient[2]
        p_manual = load_dicom(manual_file, stop_before_pixels=True)
        z_manual = p_manual.ImagePositionPatient[2]
        z_diff = z_auto - z_manual
        return z_auto, z_manual, z_diff

    def execute(self):
        auto_selected = self.input('auto_selected')
        manually_selected = self.input('manually_selected')
        nr_steps = len(auto_selected)
        data = {'file': [], 'z_auto': [], 'z_manual': [], 'z_diff': []}
        for step in range(nr_steps):
            if self.is_canceled():
                break
            auto_file = auto_selected[step]
            manual_file = self.find_manual_file(auto_file, manually_selected)
            if manual_file is not None:
                z_auto, z_manual, z_diff = self.compare_z_positions(auto_file, manual_file)
                f_name = os.path.split(manual_file)[1]
                data['file'].append(f_name)
                data['z_auto'].append(z_auto)
                data['z_manual'].append(z_manual)
                data['z_diff'].append(z_diff)
            else:
                LOG.warning(f'Could not find manually selected file for automatically selected file {auto_file}. Skipping...')
            self.set_progress(step, nr_steps)
        df = pd.DataFrame(data=data)
        csv_file_path = os.path.join(self.output('comparison'), 'comparison.csv')
        df.to_csv(csv_file_path, index=False, sep=';')