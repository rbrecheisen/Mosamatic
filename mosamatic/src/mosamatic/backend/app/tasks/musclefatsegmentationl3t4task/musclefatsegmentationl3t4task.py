import os
import json
import torch

import models

from ..task import Task
from ...utils import load_dicom, normalize_between, get_pixels_from_dicom_object, convert_labels_to_157
from .paramloader import Params


class MuscleFatSegmentationL3T4Task(Task):
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
        self.log_info('Loading models...')
        model, contour_model = None, None
        for f_path in model_files:
            f_name = os.path.split(f_path)[1]
            self.log_info(f'Checking {f_path}...')
            if f_name == f'model-{str(model_version)}.pt':
                self.log_info('Found model')
                model = models.AttentionUNet(params, 4).to(device='cpu')
                model.load_state_dict(torch.load(f_path, weights_only=False, map_location=torch.device('cpu')))
                model.eval()
                self.log_info(f'load_models_and_params() model = {model}')
            elif f_name == f'contour_model-{str(model_version)}.pt':
                self.log_info('Found contour model')
                contour_model = models.UNet(params, 2).to(device='cpu')
                contour_model.load_state_dict(torch.load(f_path, weights_only=False, map_location=torch.device('cpu')))
                contour_model.eval()
                self.log_info(f'load_models_and_params() contour_model = {contour_model}')
            else:
                pass
        return model, contour_model, params

    def execute(self):
        input_files = self.input('images')
        model_files = self.input('model_files')
        model_version = self.param('model_version', 2.0)
        model, contour_model, params = self.load_models_and_params(model_files, model_version)
        if model is None:
            raise RuntimeError('Model, contour model or parameters could not be loaded')
        nr_steps = len(input_files)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            source = input_files[step]
            self.log_info(source)
            self.set_progress(step, nr_steps)
