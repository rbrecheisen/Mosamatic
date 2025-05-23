import os
import zipfile
import shutil
import pydicom
import pydicom.errors

ZIP_DIR = 'D:\\Mosamatic\\Nicole Hildebrand\\CRLM resecties\\ZIP'
ZIP_TEMP_DIR = 'D:\\Mosamatic\\Nicole Hildebrand\\CRLM resecties\\ZIP_temp'
TARGET_DIR = 'D:\\Mosamatic\\AutomaticSliceSelection\\validation\\CRLM_resecties'


def is_dicom(f):
    try:
        pydicom.dcmread(f, stop_before_pixels=True)
        return True
    except pydicom.errors.InvalidDicomError:
        return False


def main():
    os.makedirs(ZIP_TEMP_DIR, exist_ok=True)
    for f in os.listdir(ZIP_DIR):
        if f.endswith('.zip'):
            f_path = os.path.join(ZIP_DIR, f)
            temp_path = os.path.join(ZIP_TEMP_DIR, os.path.splitext(f)[0])
            os.makedirs(temp_path, exist_ok=True)
            with zipfile.ZipFile(f_path, 'r') as zip_ref:
                zip_ref.extractall(temp_path)
            target_path = os.path.join(TARGET_DIR, os.path.splitext(f)[0])
            os.makedirs(target_path, exist_ok=True)
            for root, dirs, files in os.walk(temp_path):
                for f in files:
                    f_path = os.path.join(root, f)
                    if is_dicom(f_path):
                        shutil.copy(f_path, target_path)
            print(f'{target_path}')


if __name__ == '__main__':
    main()