from .decompressdicomfilestask.decompressdicomfilestask import DecompressDicomFilesTask
from .rescaledicomfilestask.rescaledicomfilestask import RescaleDicomFilesTask
from .musclefatsegmentationl3tensorflowtask.musclefatsegmentationl3tensorflowtask import MuscleFatSegmentationL3TensorFlowTask
from .musclefatsegmentationl3torchtask.musclefatsegmentationl3torchtask import MuscleFatSegmentationL3TorchTask
from .calculatemetricstask.calculatemetricstask import CalculateMetricsTask
from .createpngsfromdicomfilestask.createpngsfromdicomfilestask import CreatePngsFromDicomFilesTask
from .createpngsfromsegmentationstask.createpngsfromsegmentationstask import CreatePngsFromSegmentationsTask
from .totalsegmentatortask.totalsegmentatortask import TotalSegmentatorTask
from .selectslicefromscanstask.selectslicefromscanstask import SelectSliceFromScansTask
from .validatesliceselectiontask.validatesliceselectiontask import ValidateSliceSelectionTask
from .validatemusclefatsegmentationtask.validatemusclefatsegmentationtask import ValidateMuscleFatSegmentationTask
from .createpdffmapsfromdixonscanstask.createpdffmapsfromdixonscanstask import CreatePdffMapsFromDixonScansTask
from .checkdicomfilestask.checkdicomfilestask import CheckDicomFilesTask
from .anonymizedicomfilestask.anonymizedicomfilestask import AnonymizeDicomFilesTask


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
        'visible': False,
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

    'MuscleFatSegmentationL3TensorFlowTask': {
        'class': MuscleFatSegmentationL3TensorFlowTask,
        'title': 'MuscleFatSegmentationL3TensorFlowTask',
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
    
    'MuscleFatSegmentationL3TorchTask': {
        'class': MuscleFatSegmentationL3TorchTask,
        'title': 'MuscleFatSegmentationL3TorchTask',
        'description': 'Task that automatically annotates muscle and fat tissue in CT images at L3 level (uses PyTorch AI model)',
        'inputs': [
            {'name': 'images', 'label': 'Select L3 images'},
            {'name': 'model_files', 'label': 'Select model files'},
        ],
        'outputs': [
            {'name': 'segmentations', 'label': 'Enter name for segmentation output (optional)'},
        ],
        'params': [
            {'name': 'model_version', 'label': 'Select model version', 'type': 'select', 'options': [2.2]},
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
        'outputs': [
            {'name': 'metrics', 'label': 'Enter name for metrics output (optional)'},
        ],
        'params': [],
        'visible': True,
    },

    'CreatePngsFromDicomFilesTask': {
        'class': CreatePngsFromDicomFilesTask,
        'title': 'CreatePngsFromDicomFilesTask',
        'description': 'Task that generates PNG images from DICOM images',
        'inputs': [
            {'name': 'images', 'label': 'Select DICOM images'},
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
        'visible': False,
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
        'visible': False,
    },

    'ValidateMuscleFatSegmentationTask': {
        'class': ValidateMuscleFatSegmentationTask,
        'title': 'ValidateMuscleFatSegmentationTask',
        'description': 'Task that validates muscle/fat segmentations with ground truth masks',
        'inputs': [
            {'name': 'true_mask_files', 'label': 'Ground truth files'},
            {'name': 'pred_mask_files', 'label': 'Predicted segmentation files'},
        ],
        'outputs': [
            {'name': 'dice_scores', 'label': 'Enter name for output fileset containing comparison (optional)'},
        ],
        'params': [],
        'visible': True,
    },

    'CreatePdffMapsFromDixonScansTask': {
        'class': CreatePdffMapsFromDixonScansTask,
        'title': 'CreatePdffMapsFromDixonScansTask',
        'description': 'Task that creates Proton Density Fat Fraction (PDFF) maps from Dixon MRI scans',
        'inputs': [
            {'name': 'dicom_files', 'label': 'Input fileset containing Dixon MR images'},
        ],
        'outputs': [
            {'name': 'pdff_map', 'label': 'Enter name for PDFF map output (optional)'},
            {'name': 'png', 'label': 'Enter name for fileset with middle-slice PNG image (optional)'},
        ],
        'params': [],
        'visible': False,
    },

    'AnonymizeDicomFilesTask': {
        'class': AnonymizeDicomFilesTask,
        'title': 'AnonymizeDicomFilesTask',
        'description': 'Task that anonymizes DICOM files',
        'inputs': [
            {'name': 'dicom_files', 'label': 'Input fileset containing DICOM images'},
            {'name': 'recipe', 'label': 'Input fileset containing anonymization recipe (deid format)'},
        ],
        'outputs': [
            {'name': 'anonymized', 'label': 'Enter name for anonymized fileset (optional)'},
        ],
        'params': [],
        'visible': False,
    },
}