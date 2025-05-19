import os

from deid.config import DeidRecipe
from deid.dicom import replace_identifiers

from ..task import Task
from ...utils import load_dicom, is_dicom
from ...managers.logmanager import LogManager

LOG = LogManager()


class AnonymizeDicomFilesTask(Task):
    """
    TODO: Anonymize multiple scans
    """
    def execute(self):
        input_files = self.input('images')
        recipe_file = self.params('recipe_file')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            source_name = os.path.split(source)[1]
            if is_dicom(source):
                p = load_dicom(source)
                p = replace_identifiers(p, deid=DeidRecipe(recipe_file))[0]
                output_file = os.path.join(self.output('anonymized'), source_name)
                p.save_as(output_file)
                LOG.info(f'Anonymized {output_file}')
            self.set_progress(step, nr_steps)