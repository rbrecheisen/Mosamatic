import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt

DICOM_DIR = 'D:\\Mosamatic\\Maxime Dewulf Dixon + CT\\Data\\MRI'


def load_in_and_out_phase_files(dicom_dir):
    ip = []
    op = []
    for f in os.listdir(dicom_dir):
        f_path = os.path.join(dicom_dir, f)
        p = pydicom.dcmread(f_path, stop_before_pixels=True)
        if 'ImageType' in p and len(p.ImageType) > 4:
            if p.ImageType[4] == 'IN_PHASE':
                ip.append(f_path)
            if p.ImageType[4] == 'OPP_PHASE':
                op.append(f_path)
    return ip, op


def load_dicom_volume(file_paths):
    sorted_files = sorted(
        file_paths,
        key=lambda f: int(pydicom.dcmread(f, stop_before_pixels=True).InstanceNumber)
    )
    volume = []
    for path in sorted_files:
        ds = pydicom.dcmread(path)
        arr = ds.pixel_array.astype(np.float32)
        if 'RescaleSlope' in ds and 'RescaleIntercept' in ds:
            arr = arr * float(ds.RescaleSlope) + float(ds.RescaleIntercept)
        volume.append(arr)    
    return np.stack(volume, axis=0)


def main():
    ip, op = load_in_and_out_phase_files(DICOM_DIR)
    ip_volume = load_dicom_volume(ip)
    op_volume = load_dicom_volume(op)

    water_est = 0.5 * (ip_volume + op_volume)
    fat_est = 0.5 * np.abs(ip_volume - op_volume)  # abs to ensure non-negative

    pdff_est = (fat_est / (water_est + fat_est + 1e-6)) * 100

    mid_slice_idx = pdff_est.shape[0] // 2
    mid_slice = pdff_est[mid_slice_idx, :, :]

    plt.figure(figsize=(6, 6))
    plt.imshow(mid_slice, cmap='hot', vmin=0, vmax=100)
    plt.title(f"PDFF – Slice {mid_slice_idx}")
    plt.colorbar(label='PDFF (%)')
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    main()