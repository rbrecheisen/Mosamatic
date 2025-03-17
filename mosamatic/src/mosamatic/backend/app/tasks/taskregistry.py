from .decompressdicomfilestask.decompressdicomfilestask import DecompressDicomFilesTask
from .rescaledicomfilestask.rescaledicomfilestask import RescaleDicomFilesTask
from .musclefatsegmentationl3task.musclefatsegmentationl3task import MuscleFatSegmentationL3Task
from .calculatemetricstask.calculatemetricstask import CalculateMetricsTask
from .createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask


TASK_REGISTRY = {

    'DecompressDicomFilesTask': {
        'class': DecompressDicomFilesTask,
        'title': 'DecompressDicomFilesTask',
        'description': 'Task that decompresses DICOM files if needed',
        'inputs': [{'name': 'images', 'label': 'Select images'}],
        'outputs': [{'name': 'output', 'label': 'Enter name for output (optional)'}],
        'params': [],
        'visible': True,
    },

    'RescaleDicomFilesTask': {
        'class': RescaleDicomFilesTask,
        'title': 'RescaleDicomFilesTask',
        'description': 'Task that rescales DICOM images to a target size (default: 512)',
        'inputs': [{'name': 'images', 'label': 'Select images'}],
        'outputs': [{'name': 'output', 'label': 'Enter name for output (optional)'}],
        'params': [{'name': 'target_size', 'label': 'Target size', 'type': 'int', 'value': 512}],
        'visible': True,
    },

    'MuscleFatSegmentationL3Task': {
        'class': MuscleFatSegmentationL3Task,
        'title': 'MuscleFatSegmentationL3Task',
        'description': 'Task that automatically annotates muscle and fat tissue in CT images at L3 level',
        'inputs': [
            {'name': 'images', 'label': 'Select images'},
            {'name': 'model_files', 'label': 'Select model files'},
        ],
        'outputs': [{'name': 'segmentations', 'label': 'Enter name for segmentation output (optional)'}],
        'params': [
            {'name': 'model_type', 'label': 'Select model type', 'type': 'select', 'options': ['tensorflow', 'torch']},
            {'name': 'model_version', 'label': 'Select model version', 'type': 'select', 'options': [1.0]},
        ],
        'visible': True,
    },
    
    'CalculateMetricsTask': {
        'class': CalculateMetricsTask,
        'title': 'CalculateMetricsTask',
        'description': 'Task that calculates body composition metrics on automatically annotated muscle and fat regions',
        'inputs': [
            {'name': 'images', 'label': 'Select images'},
            {'name': 'segmentations', 'label': 'Select segmentations'},
            {'name': 'patient_heights', 'label': 'Select patient heights file (optional)'},
        ],
        'outputs': [{'name': 'metrics', 'label': 'Enter name for metrics output (optional)'}],
        'params': [],
        'visible': True,
    },

    'CreatePngsFromSegmentationsTask': {
        'class': CreatePngsFromSegmentationsTask,
        'title': 'CreatePngsFromSegmentationsTask',
        'description': 'Task that generates PNG images from muscle and fat annotation output',
        'inputs': [{'name': 'segmentations', 'label': 'Select segmentations'}],
        'outputs': [{'name': 'png_images', 'label': 'Enter name for PNG output (optional)'}],
        'params': [
            {'name': 'fig_width', 'label': 'Figure width', 'type': 'int', 'value': 10},
            {'name': 'fig_height', 'label': 'Figure height', 'type': 'int', 'value': 10},
        ],
        'visible': True,
    },
}