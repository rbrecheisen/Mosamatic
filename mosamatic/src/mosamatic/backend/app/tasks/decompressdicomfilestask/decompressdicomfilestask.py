import os
import shutil

from ..task import Task
from ...utils import is_jpeg2000_compressed, is_dicom, load_dicom


class DecompressDicomFilesTask(Task):
    def execute(self):
        input_files = self.input('images')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            source_name = os.path.split(source)[1]
            if is_dicom(source):
                target = os.path.join(self.output('output'), source_name)
                p = load_dicom(source)
                if is_jpeg2000_compressed(p):
                    p.decompress()
                    p.save_as(target)
                else:
                    shutil.copy(source, target)
            self.set_progress(step, nr_steps)