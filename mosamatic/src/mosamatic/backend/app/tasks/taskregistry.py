from .decompressdicomfilestask.decompressdicomfilestask import DecompressDicomFilesTask
from .rescaledicomfilestask.rescaledicomfilestask import RescaleDicomFilesTask
from .musclefatsegmentationl3task.musclefatsegmentationl3task import MuscleFatSegmentationL3Task
from .musclefatsegmentationt4pytorchtask.musclefatsegmentationt4pytorchtask import MuscleFatSegmentationT4PyTorchTask
from .calculatemetricstask.calculatemetricstask import CalculateMetricsTask
from .createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask
from .totalsegmentatortask.totalsegmentatortask import TotalSegmentatorTask
from .selectslicefromscanstask.selectslicefromscanstask import SelectSliceFromScansTask
from .createpdffmapsfromdixonscanstask.createpdffmapsfromdixonscanstask import CreatePdffMapsFromDixonScansTask


TASK_REGISTRY = {

    'DecompressDicomFilesTask': {
        'class': DecompressDicomFilesTask,
        'title': 'DecompressDicomFilesTask',
        'description': 'Task that decompresses DICOM files if needed',
        'inputs': [
            {'name': 'images', 'label': 'Select images'},
        ],
        'outputs': [
            {'name': 'output', 'label': 'Enter name for output (optional)'},
        ],
        'params': [],
        'visible': True,
    },

    'RescaleDicomFilesTask': {
        'class': RescaleDicomFilesTask,
        'title': 'RescaleDicomFilesTask',
        'description': 'Task that rescales DICOM images to a target size (default: 512)',
        'inputs': [
            {'name': 'images', 'label': 'Select images'},
        ],
        'outputs': [
            {'name': 'output', 'label': 'Enter name for output (optional)'},
        ],
        'params': [
            {'name': 'target_size', 'label': 'Target size', 'type': 'int', 'value': 512},
        ],
        'visible': True,
    },

    'MuscleFatSegmentationL3Task': {
        'class': MuscleFatSegmentationL3Task,
        'title': 'MuscleFatSegmentationL3Task',
        'description': 'Task that automatically annotates muscle and fat tissue in CT images at L3 level (uses TensorFlow AI model)',
        'inputs': [
            {'name': 'images', 'label': 'Select images'},
            {'name': 'model_files', 'label': 'Select model files'},
        ],
        'outputs': [
            {'name': 'segmentations', 'label': 'Enter name for segmentation output (optional)'},
        ],
        'params': [],
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
        'outputs': [
            {'name': 'metrics', 'label': 'Enter name for metrics output (optional)'},
        ],
        'params': [],
        'visible': True,
    },

    'CreatePngsFromSegmentationsTask': {
        'class': CreatePngsFromSegmentationsTask,
        'title': 'CreatePngsFromSegmentationsTask',
        'description': 'Task that generates PNG images from muscle and fat annotation output',
        'inputs': [
            {'name': 'segmentations', 'label': 'Select segmentations'},
        ],
        'outputs': [
            {'name': 'png_images', 'label': 'Enter name for PNG output (optional)'},
        ],
        'params': [
            {'name': 'fig_width', 'label': 'Figure width', 'type': 'int', 'value': 10},
            {'name': 'fig_height', 'label': 'Figure height', 'type': 'int', 'value': 10},
        ],
        'visible': True,
    },

    'SelectSliceFromScansTask': {
        'class': SelectSliceFromScansTask,
        'title': 'SelectSliceFromScansTask',
        'description': 'Task that automatically selects the a specific slice from CT scans using Total Segmentator',
        'inputs': [],
        'outputs': [
            {'name': 'l3_images', 'label': 'Enter name for output fileset (optional)'},
        ],
        'params': [
            {'name': 'scans', 'label': 'Input filesets', 'type': 'multi-fileset-select'},
            {'name': 'vertebra', 'label': 'Vertebral level to select', 'type': 'select', 'options': ['L3', 'T4']},
        ],
        'visible': True,
    },

    'MuscleFatSegmentationT4PyTorchTask': {
        'class': MuscleFatSegmentationT4PyTorchTask,
        'title': 'MuscleFatSegmentationT4PyTorchTask',
        'description': 'Task that automatically annotates muscle and fat tissue in CT images at T4 level (uses PyTorch AI model)',
        'inputs': [
            {'name': 'images', 'label': 'Select images'},
            {'name': 'model_files', 'label': 'Select model files'},
        ],
        'outputs': [
            {'name': 'segmentations', 'label': 'Enter name for segmentation output (optional)'},
        ],
        'params': [
            {'name': 'model_version', 'label': 'Select model version', 'type': 'select', 'options': [1.0]},
        ],
        'visible': True,
    },
    
    # EXPERIMENTAL

    'TotalSegmentatorTask': {
        'class': TotalSegmentatorTask,
        'title': 'TotalSegmentatorTask',
        'description': 'Task that runs Total Segmentator on a set of CT or MRI scans and outputs all, or selected, organ segmentations',
        'inputs': [],
        'outputs': [
            {'name': 'segmentations', 'label': 'Enter name for segmentation output (optional)'},
        ],
        'params': [
            {'name': 'scans', 'label': 'Input filesets', 'type': 'multi-fileset-select'},
            {'name': 'structures', 'label': 'Organs/structures', 'type': 'select', 'options': ['all', 'vertebrae_L3']},
        ],
        'visible': False,
    },

    'CreatePdffMapsFromDixonScansTask': {
        'class': CreatePdffMapsFromDixonScansTask,
        'title': 'CreatePdffMapsFromDixonScansTask',
        'description': 'Task that creates Proton Density Fat Fraction (PDFF) maps from multiple Dixon MRI scans',
        'inputs': [],
        'outputs': [
            {'name': 'pdff_maps', 'label': 'Enter name for PDFF map output (optional)'},
        ],
        'params': [
            {'name': 'scans', 'label': 'Input filesets', 'type': 'multi-fileset-select'},
        ],
        'visible': False,
    },
}