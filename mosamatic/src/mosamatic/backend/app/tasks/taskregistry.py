from .exampletask.exampletask import ExampleTask
from .copyfilestask.copyfilestask import CopyFilesTask
from .mergedirectoriestask.mergedirectoriestask import MergeDirectoriesTask
from .decompressdicomfilestask.decompressdicomfilestask import DecompressDicomFilesTask
from .rescaledicomfilestask.rescaledicomfilestask import RescaleDicomFilesTask
from .musclefatsegmentationl3task.musclefatsegmentationl3task import MuscleFatSegmentationL3Task
from .calculatemetricstask.calculatemetricstask import CalculateMetricsTask
from .createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask


TASK_REGISTRY = {

    'ExampleTask': {
        'class': ExampleTask,
        'title': 'ExampleTask',
        'description': 'Example Task with two inputs and one output',
        'inputs': [
            {'name': 'input1', 'label': 'Select input 1'},
            {'name': 'input2', 'label': 'Select input 2'},
        ],
        'outputs': [{'name': 'output1', 'label': 'Enter name for output (optional)'}],
        'params': [
            {'name': 'nr_iters', 'label': 'Number of iterations', 'type': 'int', 'min': 0, 'max': 100, 'step': 1, 'value': 5},
            {'name': 'delay', 'label': 'Delay (s)', 'type': 'int', 'min': 0, 'max': 10, 'step': 1, 'value': 1},
        ],
    },
    
    'CopyFilesTask': {
        'class': CopyFilesTask,
        'title': 'CopyFilesTask',
        'description': 'Task that copies files from an input to an output directory',
        'inputs': [{'name': 'input1', 'label': 'Select input 1'}],
        'outputs': [{'name': 'output1', 'label': 'Enter name for output (optional)'}],
        'params': [],
    },
    
    'MergeDirectoriesTask': {
        'class': MergeDirectoriesTask,
        'title': 'MergeDirectoriesTask',
        'description': 'Task that copies files from two input directories to a single output directory',
        'inputs': [
            {'name': 'input1', 'label': 'Select input 1'},
            {'name': 'input2', 'label': 'Select input 2'},
        ],
        'outputs': [{'name': 'output1', 'label': 'Enter name for output (optional)'}],
        'params': [{'name': 'keep_duplicates', 'label': 'Keep duplicates in merge (appends number if needed)', 'type': 'bool', 'value': False}],
    },

    'DecompressDicomFilesTask': {
        'class': DecompressDicomFilesTask,
        'title': 'DecompressDicomFilesTask',
        'description': 'Task that decompresses DICOM files if needed',
        'inputs': [{'name': 'images', 'label': 'Select images'}],
        'outputs': [{'name': 'output', 'label': 'Enter name for output (optional)'}],
        'params': [],
    },

    'RescaleDicomFilesTask': {
        'class': RescaleDicomFilesTask,
        'title': 'RescaleDicomFilesTask',
        'description': 'Task that rescales DICOM images to a target size (default: 512)',
        'inputs': [{'name': 'images', 'label': 'Select images'}],
        'outputs': [{'name': 'output', 'label': 'Enter name for output (optional)'}],
        'params': [{'name': 'target_size', 'label': 'Target size', 'type': 'int', 'value': 512}]
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
        ]
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
    },
}