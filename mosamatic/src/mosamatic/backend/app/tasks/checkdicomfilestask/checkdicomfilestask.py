import os

from ..task import Task
from ...utils import load_dicom, is_jpeg2000_compressed, get_pixels_from_dicom_object
from ...managers.logmanager import LogManager

LOG = LogManager()


class CheckDicomFilesTask(Task):
    def execute(self):
        input_files = self.input('images')
        nr_steps = len(input_files)
        errors = []
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            source_name = os.path.split(source)[1]
            p = load_dicom(source)
            if is_jpeg2000_compressed(p):
                p.decompress()
            pixels = get_pixels_from_dicom_object(p)
            if len(pixels.shape) != 2:
                message = f'File {source} pixel array has wrong shape ({pixels.shape})'
                errors.append(message)
                LOG.warning(message)
            self.set_progress(step, nr_steps)
        if len(errors) > 0:
            with open(os.path.join(self.output('output'), 'errors.txt'), 'w') as f:
                for error in errors:
                    f.write(error + '\n')