import os
import re
import json
import uuid
import pydicom

from collections import defaultdict
from typing import Union, List
from django.conf import settings
from django.http import HttpRequest
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from ..managers.logmanager import LogManager
from ..managers.datamanager import DataManager
from ..utils import is_dicom, create_name_with_timestamp

LOG = LogManager()


class FileUploadManager:

    # def is_dixon(self, description):
    #     return "dixon" in description or any(tag in description for tag in ["water", "fat", "ip", "op", "inphase", "outphase"])
    # def normalize_dixon_series_description(self, description):
    #     return re.sub(r'\b(water|fat|in[-_ ]?phase|out[-_ ]?phase|ip|op)\b', '', description, flags=re.IGNORECASE).strip()
    # def extract_group_key(self, p):
    #     description = p.get('SeriesDescription', '').lower()
    #     acquisition_time = p.get('AcquisitionTime', '')[:4]
    #     if self.is_dixon(description):
    #         description = self.normalize_dixon_series_description(description)
    #         return f'DIXON::{description}::{acquisition_time}'
    #     return f'{p.Modality}::{description}::{acquisition_time}'
    
    def process_upload(self, request, fileset_name, single_fileset=True):
        data_manager = DataManager()
        if single_fileset:
            fileset = data_manager.create_fileset(request.user, fileset_name)
            for _, f in request.FILES.items():
                with open(f.temporary_file_path(), 'rb') as f_obj:
                    f_path = default_storage.save(f'{fileset.id()}/{f.name}', ContentFile(f_obj.read()))
                    f_path = os.path.join(settings.MEDIA_ROOT, f_path)
                    data_manager.create_file(f_path, fileset)
                    LOG.info(f'Added file {f_path}')
        else:
            filesets = defaultdict(list)
            LOG.info('Collecting temporary files and grouping in series...')
            for rel_path, f in request.FILES.items():
                temp_path = f.temporary_file_path()
                scan_dir_name = rel_path.split('/')[-2]
                if is_dicom(temp_path):
                    p = pydicom.dcmread(temp_path, stop_before_pixels=True)
                    if p.Modality in ['CT', 'MR']:
                        filesets[p.SeriesInstanceUID].append({
                            'file_name': f.name, 
                            'file_path': temp_path, 
                            'scan_dir_name': scan_dir_name,
                            'modality': p.Modality,
                            'series_description': p.SeriesDescription,
                        })
                else:
                    LOG.warning(f'Skipping non-DICOM file {temp_path}')
            for _, file_list in filesets.items():
                fileset_name = '{}'.format(file_list[0]['scan_dir_name'])
                fileset = data_manager.create_fileset(request.user, name=fileset_name)
                for entry in file_list:
                    with open(entry['file_path'], 'rb') as f:
                        f_path = default_storage.save('{}/{}'.format(fileset.id(), entry['file_name']), ContentFile(f.read()))
                        f_path = os.path.join(settings.MEDIA_ROOT, f_path)
                        data_manager.create_file(f_path, fileset)
                        LOG.info(f'Added file {f_path} to fileset {fileset.name()}')