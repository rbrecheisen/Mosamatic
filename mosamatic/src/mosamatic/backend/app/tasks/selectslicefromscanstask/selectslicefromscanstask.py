import os
import shutil
import math
import tempfile
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt


from ...utils import load_dicom
from ...managers.datamanager import DataManager
from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()

VERTEBRA = 'vertebrae_L3'

TOTAL_SEGMENTATOR_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), 'total_segmentator_output')


class SelectSliceFromScansTask(Task):
    def extract_masks(self, scan_dir):
        os.makedirs(TOTAL_SEGMENTATOR_OUTPUT_DIR, exist_ok=True)
        os.system(f'TotalSegmentator -i {scan_dir} -o {TOTAL_SEGMENTATOR_OUTPUT_DIR} --fast')

    def delete_total_segmentator_output(self):
        if os.path.exists(TOTAL_SEGMENTATOR_OUTPUT_DIR):
            shutil.rmtree(TOTAL_SEGMENTATOR_OUTPUT_DIR)

    def find_l3(self, scan_dir, mask_name):
        # Find Z-positions DICOM images
        z_positions = {}
        for f in os.listdir(scan_dir):
            f_path = os.path.join(scan_dir, f)
            p = load_dicom(f_path, stop_before_pixels=True)
            if p is not None:
                z_positions[p.ImagePositionPatient[2]] = f_path
        # Find Z-position L3 image
        mask_file = os.path.join(TOTAL_SEGMENTATOR_OUTPUT_DIR, f'{mask_name}.nii.gz')
        mask_obj = nib.load(mask_file)
        mask = mask_obj.get_fdata()
        affine_transform = mask_obj.affine
        indexes = np.array(np.where(mask == 1))
        index_min = indexes.min(axis=1)
        index_max = indexes.max(axis=1)
        world_min = nib.affines.apply_affine(affine_transform, index_min)
        world_max = nib.affines.apply_affine(affine_transform, index_max)
        z_direction = affine_transform[:3, 2][2]
        z_sign = math.copysign(1, z_direction)
        z_delta = 0.333 * abs(world_max[2] - world_min[2])
        z_l3 = world_max[2] - z_sign * z_delta
        # Find closest L3 image in DICOM set
        positions = sorted(z_positions.keys())
        closest_file = None
        for z1, z2 in zip(positions[:-1], positions[1:]):
            if min(z1, z2) <= z_l3 <= max(z1, z2):
                closest_z = min(z_positions.keys(), key=lambda z: abs(z - z_l3))
                closest_file = z_positions[closest_z]
                print(f'Closest image: {closest_file}')
                break
        return closest_file

    def execute(self):
        scans = self.param('scans')
        vertebral_level = self.param('vertebral_level')
        data_manager = DataManager()
        nr_steps = len(scans)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            fileset_id = scans[step]
            fileset = data_manager.fileset(fileset_id)
            scan_dir = fileset.path()
            self.extract_masks(scan_dir)
            file_path = self.find_l3(scan_dir, vertebral_level)
            if file_path is not None:
                extension = '' if file_path.endswith('.dcm') else '.dcm'
                target_file_path = os.path.join(self.output('selected_images'), f'{vertebral_level}_' + fileset.name() + extension)
                shutil.copyfile(file_path, target_file_path)
            self.delete_total_segmentator_output()
            self.set_progress(step, nr_steps)