import os
import shutil
import numpy as np

from scipy.ndimage import zoom

from ..task import Task
from ...utils import load_dicom


class RescaleDicomFilesTask(Task):
    def rescale_image(self, p, target_size):
        pixel_array = p.pixel_array
        hu_array = pixel_array * p.RescaleSlope + p.RescaleIntercept
        hu_air = -1000
        new_rows = max(p.Rows, p.Columns)
        new_cols = max(p.Rows, p.Columns)
        padded_hu_array = np.full((new_rows, new_cols), hu_air, dtype=hu_array.dtype)
        padded_hu_array[:pixel_array.shape[0], :pixel_array.shape[1]] = hu_array
        pixel_array_padded = (padded_hu_array - p.RescaleIntercept) / p.RescaleSlope
        pixel_array_padded = pixel_array_padded.astype(pixel_array.dtype) # Image now has largest dimensions
        pixel_array_rescaled = zoom(pixel_array_padded, zoom=(target_size / new_rows), order=3) # Cubic interpolation
        pixel_array_rescaled = pixel_array_rescaled.astype(pixel_array.dtype)
        original_pixel_spacing = p.PixelSpacing
        new_pixel_spacing = [ps * (new_rows / target_size) for ps in original_pixel_spacing]
        p.PixelSpacing = new_pixel_spacing
        p.PixelData = pixel_array_rescaled.tobytes()
        p.Rows = target_size
        p.Columns = target_size
        return p

    def execute(self):
        target_size = self.param('target_size', 512)
        input_files = self.input('input')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            source_name = os.path.split(source)[1]
            p = load_dicom(source)
            if p.Rows != target_size or p.Columns != target_size:
                p = self.rescale_image(p, target_size)
                source_name = os.path.splitext(source_name)[0] + '_rescaled.dcm'
                target = os.path.join(self.output('output'), source_name)
                p.save_as(target)
            else:
                target = os.path.join(self.output('output'), source_name)
                shutil.copy(source, target)
            self.set_progress(step, nr_steps)