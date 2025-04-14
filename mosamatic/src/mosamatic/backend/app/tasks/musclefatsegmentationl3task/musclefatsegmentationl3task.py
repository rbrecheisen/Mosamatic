import os
import numpy as np

from ..task import Task
from .tensorflowmodel import TensorFlowModel
# from .torchmodel import TorchModel
from ...utils import load_dicom, is_jpeg2000_compressed, normalize_between, get_pixels_from_dicom_object, convert_labels_to_157


class MuscleFatSegmentationL3Task(Task):
    def load_models_and_params(self, model_files, model_type, model_version):
        # if model_type == 'torch':
        #     torch_model = TorchModel()
        #     model, contour_model, params = torch_model.load(model_files, model_version)
        #     return model, contour_model, params
        if model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            model, contour_model, params = tensorflow_model.load(model_files, model_version)
            return model, contour_model, params
        else:
            raise RuntimeError(f'Unknown model type {model_type}')

    def predict_contour(self, contour_model, img, params, model_type):
        # if model_type == 'torch':
        #     torch_model = TorchModel()
        #     mask = torch_model.predict_contour(img, contour_model, params)
        #     return mask
        if model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            mask = tensorflow_model.predict_contour(img, contour_model, params)
            return mask
        else:
            raise RuntimeError(f'Unknown model type {model_type}')

    def process_file(self, f_path, output_dir, model, contour_model, params, model_type):
        p = load_dicom(f_path)
        if p is None:
            self.log_warning(f'File {f_path} is not valid DICOM, skipping...')
            return
        if is_jpeg2000_compressed(p):
            p.decompress()
        img1 = get_pixels_from_dicom_object(p, normalize=True)        
        if contour_model:
            mask = self.predict_contour(contour_model, img1, params, model_type)
            img1 = normalize_between(img1, params['min_bound'], params['max_bound'])
            img1 = img1 * mask
        img1 = img1.astype(np.float32)
        # if model_type == 'torch':
        #     torch_model = TorchModel()
        #     pred_max = torch_model.predict(img1, model)
        if model_type == 'tensorflow':
            tensorflow_model = TensorFlowModel()
            pred_max = tensorflow_model.predict(img1, model)
        else:
            raise RuntimeError(f'Unknown model type {model_type}')
        pred_max = convert_labels_to_157(pred_max)
        segmentation_file_name = os.path.split(f_path)[1]
        segmentation_file_path = os.path.join(output_dir, f'{segmentation_file_name}.seg.npy')
        np.save(segmentation_file_path, pred_max)
        return segmentation_file_path

    def execute(self):
        input_files = self.input('images')
        model_files = self.input('model_files')
        model_type = self.param('model_type', 'tensorflow')
        model_version = self.param('model_version', 1.0)
        model, contour_model, params = self.load_models_and_params(model_files, model_type, model_version)
        if model is None or contour_model is None or params is None:
            raise RuntimeError('Model, contour model or parameters could not be loaded')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            self.process_file(source, self.output('segmentations'), model, contour_model, params, model_type)
            self.set_progress(step, nr_steps)