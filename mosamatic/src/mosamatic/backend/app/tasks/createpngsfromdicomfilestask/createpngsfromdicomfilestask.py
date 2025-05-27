import os

from ..task import Task
from ...utils import convert_dicom_to_numpy_array, convert_numpy_array_to_png_image


class CreatePngsFromDicomFilesTask(Task):
    def execute(self):
        input_files = self.input('images')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            source_name = os.path.split(source)[1]
            png_file_name = source_name + '.png'
            source_image = convert_dicom_to_numpy_array(source)
            png_file_name = source_name + '.png'
            convert_numpy_array_to_png_image(
                source_image, 
                self.output('png_images'),
                png_file_name=png_file_name,
                fig_width=self.param('fig_width', 10),
                fig_height=self.param('fig_height', 10),
            )
            self.set_progress(step, nr_steps)