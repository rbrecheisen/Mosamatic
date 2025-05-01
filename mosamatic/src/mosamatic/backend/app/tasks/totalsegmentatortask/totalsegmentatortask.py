import os
import shutil
import tempfile

from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()

TOTAL_SEGMENTATOR_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), 'total_segmentator_output')
LOG.info(f'TOTAL_SEGMENTATOR_OUTPUT_DIR: {TOTAL_SEGMENTATOR_OUTPUT_DIR}')


class TotalSegmentatorTask(Task):
    def extract_masks(self, scan_dir, task, fast):
        fast = '--fast' if fast else ''
        os.makedirs(TOTAL_SEGMENTATOR_OUTPUT_DIR, exist_ok=True)
        os.system(f'TotalSegmentator -i {scan_dir} -o {TOTAL_SEGMENTATOR_OUTPUT_DIR} -ta {task} {fast}')

    def delete_total_segmentator_output(self):
        if os.path.exists(TOTAL_SEGMENTATOR_OUTPUT_DIR):
            shutil.rmtree(TOTAL_SEGMENTATOR_OUTPUT_DIR)

    def execute(self):
        input_files = self.input('scan')
        task = self.param('task')
        task = 'total' if task == 'all' else task
        fast = self.param('fast')
        scan_dir = None
        if len(input_files) > 0:
            scan_dir = os.path.split(input_files[0])[0]
        if scan_dir is None:
            self.cancel()
            return
        self.extract_masks(scan_dir, task, fast)
        for f in os.listdir(TOTAL_SEGMENTATOR_OUTPUT_DIR):
            f_path = os.path.join(TOTAL_SEGMENTATOR_OUTPUT_DIR, f)
            target_f_path = os.path.join(self.output('segmentations'), f)
            shutil.copyfile(f_path, target_f_path)
        self.delete_total_segmentator_output()
        self.set_progress(1, 1)