import os
import numpy as np

import models

from ..task import Task
from ...utils import load_dicom, normalize_between, get_pixels_from_dicom_object, convert_labels_to_157


class MuscleFatSegmentationL3T4Task(Task):
    pass