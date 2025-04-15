from ..task import Task


class TotalSegmentatorTask(Task):
    def execute(self):
        scans = self.param('scans')
        structures = self.param('structures')
        print(f'scans: {scans}, structures: {structures}')