from totalsegmentator.python_api import totalsegmentator

from ...managers.datamanager import DataManager
from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()


class TotalSegmentatorTask(Task):
    def execute(self):
        scans = self.param('scans')
        structures = self.param('structures')
        data_manager = DataManager()
        for fileset_id in scans:
            fileset = data_manager.fileset(fileset_id)
            fileset_path = fileset.path()
            LOG.info(f'Running TS on {fileset.name()}...')
            totalsegmentator(fileset_path, 'D:\\Mosamatic\\TotalSegmentatorOutput', fast=True)
            break