import os
import numpy as np

from ..task import Task
from ...utils import convert_numpy_array_to_png_image, AlbertaColorMap


class CreatePngsFromSegmentationsTask(Task):
    def execute(self):
        input_files = self.input('segmentations')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            source_name = os.path.split(source)[1]
            source_image = np.load(source)
            png_file_name = source_name + '.png'
            convert_numpy_array_to_png_image(
                source_image, 
                self.output('png_images'),
                AlbertaColorMap(), 
                png_file_name,
                fig_width=self.param('fig_width', 10),
                fig_height=self.param('fig_height', 10),
            )
            self.set_progress(step, nr_steps)