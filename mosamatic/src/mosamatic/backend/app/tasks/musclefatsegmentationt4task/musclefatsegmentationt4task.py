import os
import torch
import numpy as np

import models

from ..task import Task
from ...utils import load_dicom, is_jpeg2000_compressed, normalize_between, get_pixels_from_dicom_object, convert_labels_to_157
from .paramloader import Params

DEVICE = 'cpu'


class MuscleFatSegmentationT4Task(Task):
    def load_models_and_params(self, model_files, model_version):
        # First load params.json because it is needed to instantiate the models
        params = None
        for f_path in model_files:
            f_name = os.path.split(f_path)[1]
            if f_name == f'params-{str(model_version)}.json':
                params = Params(f_path)
                break
        if params is None:
            raise RuntimeError('Could not load parameters')
        # Next, load models
        model, contour_model = None, None
        for f_path in model_files:
            f_name = os.path.split(f_path)[1]
            if f_name == f'model-{str(model_version)}.pt':
                model = models.AttentionUNet(params, 4).to(device=DEVICE)
                model.load_state_dict(torch.load(f_path, weights_only=False, map_location=torch.device(DEVICE)))
                model.eval()
            elif f_name == f'contour_model-{str(model_version)}.pt':
                contour_model = models.UNet(params, 2).to(device=DEVICE)
                contour_model.load_state_dict(torch.load(f_path, weights_only=False, map_location=torch.device(DEVICE)))
                contour_model.eval()
            else:
                pass
        return model, contour_model, params
    
    def extract_contour(self, image, contour_model):
        with torch.no_grad():
            # Create 4D Tensor input
            input = np.expand_dims(image, 0)
            input = np.expand_dims(input, 0)
            input = torch.Tensor(input)
            input = input.to(DEVICE, dtype=torch.float)
            # Predict
            prediction = contour_model(input)
            prediction = torch.argmax(prediction, axis=1)
            prediction = prediction.squeeze()
            prediction = prediction.detach().cpu().numpy()
        return image * prediction
    
    def segment_muscle_and_fat(self, image, model):
        input = np.expand_dims(image, 0)
        input = np.expand_dims(input, 0)
        input = torch.Tensor(input)
        input = input.to(DEVICE, dtype=torch.float)
        segmentation = model(input)
        segmentation = torch.argmax(segmentation, axis=1)
        segmentation = segmentation.squeeze()
        segmentation = segmentation.detach().cpu().numpy()
        return segmentation
    
    def process_file(self, f_path, output_dir, model, contour_model, params):
        p = load_dicom(f_path)
        if p is None:
            self.log_warning(f'File {f_path} is not valid DICOM, skipping...')
            return
        if is_jpeg2000_compressed(p):
            p.decompress()
        image = get_pixels_from_dicom_object(p, normalize=True)
        image = normalize_between(image, params.dict['lower_bound'], params.dict['upper_bound'])
        image = self.extract_contour(image, contour_model)
        segmentation = self.segment_muscle_and_fat(image, model)
        segmentation = convert_labels_to_157(segmentation)
        segmentation_file_name = os.path.split(f_path)[1]
        segmentation_file_path = os.path.join(output_dir, f'{segmentation_file_name}.seg.npy')
        np.save(segmentation_file_path, segmentation)

    def execute(self):
        input_files = self.input('images')
        model_files = self.input('model_files')
        model_version = self.param('model_version', 1.0)
        model, contour_model, params = self.load_models_and_params(model_files, model_version)
        if model is None:
            raise RuntimeError('Model, contour model or parameters could not be loaded')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            self.process_file(source, self.output('segmentations'), model, contour_model, params)
            self.set_progress(step, nr_steps)
