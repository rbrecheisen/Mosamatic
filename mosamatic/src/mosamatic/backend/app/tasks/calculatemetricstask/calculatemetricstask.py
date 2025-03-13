import os
import csv
import numpy as np
import pandas as pd

from ..task import Task
from ...utils import calculate_area, calculate_index, calculate_mean_radiation_attenuation, get_pixels_from_dicom_object, load_dicom

MUSCLE, VAT, SAT = 1, 5, 7


class CalculateMetricsTask(Task):
    def collect_img_seg_pairs(self, image_files, segmentation_files):
        img_seg_pairs = []
        for f_img_path in image_files:
            f_img_name = os.path.split(f_img_path)[1]
            for f_seg_path in segmentation_files:
                f_seg_name = os.path.split(f_seg_path)[1]
                if f_seg_name.removesuffix('.seg.npy') == f_img_name:
                    img_seg_pairs.append((f_img_path, f_seg_path))
        return img_seg_pairs
    
    def load_patient_heights(self, f):
        with open(f, mode='r', encoding='utf-8') as f_obj:
            reader = csv.DictReader(f_obj)
            return [row for row in reader]
        
    def get_patient_height(self, file_name, patient_heights):
        for row in patient_heights:
            if row['file'] in file_name:
                return float(row['height'])
        return None
    
    def load_image(self, f):
        p = load_dicom(f)
        if p is None:
            return None, None
        pixels = get_pixels_from_dicom_object(p, normalize=True)
        return pixels, p.PixelSpacing

    def load_segmentation(self, f):
        return np.load(f)

    def execute(self):
        image_files = self.input('images')
        segmentation_files = self.input('segmentations')
        img_seg_pairs = self.collect_img_seg_pairs(image_files, segmentation_files)
        patient_heights = None
        patient_heights_file = self.input('patient_heights')
        if patient_heights_file:
            patient_height_file = patient_height_file[0]
            patient_heights = self.load_patient_heights(patient_height_file)
        # Create empty data dictionary
        data = {
            'file': [], 
            'muscle_area': [], 'muscle_idx': [], 'muscle_ra': [],
            'vat_area': [], 'vat_idx': [], 'vat_ra': [],
            'sat_area': [], 'sat_idx': [], 'sat_ra': []
        }
        nr_steps = len(img_seg_pairs)
        for step in range(nr_steps):
            if self.is_canceled():
                break
            # Get image and its pixel spacing
            image, pixel_spacing = self.load_image(img_seg_pairs[step][0])
            if image is None:
                raise RuntimeError(f'Could not load DICOM image for file {img_seg_pairs[step][0]}')
            # Get segmentation for this image
            segmentation = self.load_segmentation(img_seg_pairs[step][1])
            if segmentation is None:
                raise RuntimeError(f'Could not load segmentation for file {img_seg_pairs[step][1]}')
            # Calculate metrics
            file_name = os.path.split(img_seg_pairs[step][0])[1]
            muscle_area = calculate_area(segmentation, MUSCLE, pixel_spacing)
            muscle_idx = 0
            if patient_heights:
                muscle_idx = calculate_index(muscle_area, self.get_patient_height(file_name, patient_heights))
            muscle_ra = calculate_mean_radiation_attenuation(image, segmentation, MUSCLE)
            vat_area = calculate_area(segmentation, VAT, pixel_spacing)
            vat_idx = 0
            if patient_heights:
                vat_idx = calculate_index(vat_area, self.get_patient_height(file_name, patient_heights))
            vat_ra = calculate_mean_radiation_attenuation(image, segmentation, VAT)
            sat_area = calculate_area(segmentation, SAT, pixel_spacing)
            sat_idx = 0
            if patient_heights:
                sat_idx = calculate_index(sat_area, self.get_patient_height(file_name, patient_heights))
            sat_ra = calculate_mean_radiation_attenuation(image, segmentation, SAT)
            self.log_info(f'file: {file_name}, ' +
                    f'muscle_area: {muscle_area}, muscle_idx: {muscle_idx}, muscle_ra: {muscle_ra}, ' +
                    f'vat_area: {vat_area}, vat_idx: {vat_idx}, vat_ra: {vat_ra}, ' +
                    f'sat_area: {sat_area}, sat_idx: {sat_idx}, sat_ra: {sat_ra}')
            # Update dataframe data
            data['file'].append(file_name)
            data['muscle_area'].append(muscle_area)
            data['muscle_idx'].append(muscle_idx)
            data['muscle_ra'].append(muscle_ra)
            data['vat_area'].append(vat_area)
            data['vat_idx'].append(vat_idx)
            data['vat_ra'].append(vat_ra)
            data['sat_area'].append(sat_area)
            data['sat_idx'].append(sat_idx)
            data['sat_ra'].append(sat_ra)
            # Update progress
            self.set_progress(step, nr_steps)
        # Build dataframe and return the CSV file as output
        csv_file_path = os.path.join(self.output('metrics'), 'bc_metrics.csv')
        df = pd.DataFrame(data=data)
        df.to_csv(csv_file_path, index=False, sep=';')