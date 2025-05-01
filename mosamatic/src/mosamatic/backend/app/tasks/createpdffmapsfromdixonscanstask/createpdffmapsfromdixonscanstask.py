import os
import pydicom
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()


class CreatePdffMapFromDixonScanTask(Task):
    def get_in_and_out_phase_images(self, files):
        ip = []
        op = []
        for f_path in files:
            p = pydicom.dcmread(f_path, stop_before_pixels=True)
            if 'ImageType' in p and len(p.ImageType) > 4:
                if p.ImageType[4] == 'IN_PHASE':
                    ip.append(f_path)
                if p.ImageType[4] == 'OPP_PHASE':
                    op.append(f_path)
        return ip, op

    def load_dicom_volume(self, files):
        sorted_files = sorted(
            files,
            key=lambda f: int(pydicom.dcmread(f, stop_before_pixels=True).InstanceNumber)
        )
        volume = []
        for path in sorted_files:
            ds = pydicom.dcmread(path)
            arr = ds.pixel_array.astype(np.float32)
            if 'RescaleSlope' in ds and 'RescaleIntercept' in ds:
                arr = arr * float(ds.RescaleSlope) + float(ds.RescaleIntercept)
            volume.append(arr)    
        return np.stack(volume, axis=0)

    def execute(self):
        input_files = self.input('dicom_files')
        ip, op = self.get_in_and_out_phase_images(input_files)
        ip_volume = self.load_dicom_volume(ip)
        op_volume = self.load_dicom_volume(op)
        water = 0.5 * (ip_volume + op_volume)
        fat = 0.5 * np.abs(ip_volume - op_volume)  # abs to ensure non-negative
        pdff_map = (fat / (water + fat + 1e-6)) * 100
        # Save PDFF map to output fileset
        pdff_map_file_path = os.path.join(self.output('pdff_map'), 'pdff_map.npy')
        np.save(pdff_map_file_path, pdff_map)
        # Create PNG image of middle slice and save to PNG output fileset
        mid_slice_idx = pdff_map.shape[0] // 2
        mid_slice = pdff_map[mid_slice_idx, :, :]
        mid_slice_norm = np.clip(mid_slice, 0, 100)  # Clamp to expected vmin/vmax
        mid_slice_uint8 = ((mid_slice_norm / 100) * 255).astype(np.uint8)
        scale_factor = 4  # e.g., 4x bigger
        image = Image.fromarray(mid_slice_uint8, mode='L')
        image_resized = image.resize(
            (image.width * scale_factor, image.height * scale_factor),
            resample=Image.BICUBIC
        )
        pdff_png_file_path = os.path.join(self.output('png'), 'pdff_map.png')
        image_resized.save(pdff_png_file_path)
        self.set_progress(0, 1)