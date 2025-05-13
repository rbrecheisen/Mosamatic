from .decompressdicomfilestask.decompressdicomfilestask import DecompressDicomFilesTask
from .rescaledicomfilestask.rescaledicomfilestask import RescaleDicomFilesTask
from .musclefatsegmentationl3task.musclefatsegmentationl3task import MuscleFatSegmentationL3Task
from .musclefatsegmentationt4task.musclefatsegmentationt4task import MuscleFatSegmentationT4Task
from .calculatemetricstask.calculatemetricstask import CalculateMetricsTask
from .createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask
from .totalsegmentatortask.totalsegmentatortask import TotalSegmentatorTask
from .selectslicefromscanstask.selectslicefromscanstask import SelectSliceFromScansTask
from .validatesliceselectiontask.validatesliceselectiontask import ValidateSliceSelectionTask
from .createpdffmapsfromdixonscanstask.createpdffmapsfromdixonscanstask import CreatePdffMapFromDixonScanTask
from .checkdicomfilestask.checkdicomfilestask import CheckDicomFilesTask


TASK_REGISTRY = {

    'CheckDicomFilesTask': {
        'class': CheckDicomFilesTask,
        'title': 'CheckDicomFilesTask',
        'description': 'Task that checks DICOM images for muscle/fat segmentation, specifically NumPy array shape',
        'inputs': [
            {'name': 'images', 'label': 'Select images'},
        ],
        'outputs': [
            {'name': 'output', 'label': 'Enter name for output (optional)'},
        ],
        'params': [],
        'visible': True,
    },

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

    'TotalSegmentatorTask': {
        'class': TotalSegmentatorTask,
        'title': 'TotalSegmentatorTask',
        'description': 'Task that runs Total Segmentator on a single CT scan and extracts various structures',
        'inputs': [
            {'name': 'scan', 'label': 'Select scan'},
        ],
        'outputs': [
            {'name': 'segmentations', 'label': 'Enter name for segmentation output (optional)'},
        ],
        'params': [
            {'name': 'task', 'label': 'Task to run', 'type': 'select', 'options': ['all', 'liver_vessels', 'liver_segments']},
            {'name': 'fast', 'label': 'Use fast option', 'type': 'bool', 'default': True},
        ],
        'visible': True,
    },

    'SelectSliceFromScansTask': {
        'class': SelectSliceFromScansTask,
        'title': 'SelectSliceFromScansTask',
        'description': 'Task that automatically selects a vertebral slice from a set of CT scans using Total Segmentator',
        'inputs': [],
        'outputs': [
            {'name': 'selected_images', 'label': 'Enter name for output fileset (optional)'},
        ],
        'params': [
            {'name': 'scans', 'label': 'Input filesets', 'type': 'multi-fileset-select'},
            {'name': 'vertebral_level', 'label': 'Vertebral level', 'type': 'select', 'options': ['vertebrae_L3', 'vertebrae_T4']},
        ],
        'visible': True,
    },

    'ValidateSliceSelectionTask': {
        'class': ValidateSliceSelectionTask,
        'title': 'ValidateSliceSelectionTask',
        'description': 'Task that validates automatic slice selection (from SelectSliceFromScansTask) with manual selections',
        'inputs': [
            {'name': 'auto_selected', 'label': 'Automatically selected images'},
            {'name': 'manually_selected', 'label': 'Ground truth manually selected images'},
        ],
        'outputs': [
            {'name': 'comparison', 'label': 'Enter name for output fileset containing comparison (optional)'},
        ],
        'params': [],
        'visible': True,
    },

    'MuscleFatSegmentationT4Task': {
        'class': MuscleFatSegmentationT4Task,
        'title': 'MuscleFatSegmentationT4Task',
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
    
    'CreatePdffMapFromDixonScanTask': {
        'class': CreatePdffMapFromDixonScanTask,
        'title': 'CreatePdffMapFromDixonScanTask',
        'description': 'Task that creates a Proton Density Fat Fraction (PDFF) map from a single Dixon MRI scan',
        'inputs': [
            {'name': 'dicom_files', 'label': 'Input fileset containing Dixon MR images'},
        ],
        'outputs': [
            {'name': 'pdff_map', 'label': 'Enter name for PDFF map output (optional)'},
            {'name': 'png', 'label': 'Enter name for fileset with middle-slice PNG image (optional)'},
        ],
        'params': [],
        'visible': True,
    },
}