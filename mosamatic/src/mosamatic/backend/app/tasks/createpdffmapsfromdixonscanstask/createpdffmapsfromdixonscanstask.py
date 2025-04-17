from ...managers.datamanager import DataManager
from ...managers.logmanager import LogManager
from ..task import Task

LOG = LogManager()


class CreatePdffMapsFromDixonScansTask(Task):
    def execute(self):
        scans = self.param('scans')
        data_manager = DataManager()
        for fileset_id in scans:
            fileset = data_manager.fileset(fileset_id)
            fileset_path = fileset.path()
            LOG.info(f'Creating PDFF map from {fileset.name()}...')