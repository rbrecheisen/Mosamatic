import os
import math
import pydicom
import nibabel as nib
import datetime
import numpy as np
import matplotlib.pyplot as plt

from totalsegmentator.python_api import totalsegmentator

SCAN_DIR = 'D:\\Mosamatic\\AutomaticSliceSelection\\scans\\scan1'
OUTPUT_DIR = 'D:\\Mosamatic\\AutomaticSliceSelection\\output'
MASK_FILE = 'vertebrae_L3.nii.gz'
FAST = True

TRUE_L3 = 'D:\Mosamatic\AutomaticSliceSelection\scans\scan1\CT.1.3.12.2.1107.5.1.4.75537.30000020012407082293400013618'
CLOSEST = 'D:\Mosamatic\AutomaticSliceSelection\scans\scan1\CT.1.3.12.2.1107.5.1.4.75537.30000020012407082293400013618'
CLOSEST_GPU = 'D:\Mosamatic\AutomaticSliceSelection\scans\scan1\CT.1.3.12.2.1107.5.1.4.75537.30000020012407082293400013619'


def main():
    print('Collecting DICOM Z-positions...')
    z_positions = {}
    for f in os.listdir(SCAN_DIR):
        f_path = os.path.join(SCAN_DIR, f)
        p = pydicom.dcmread(f_path, stop_before_pixels=True)
        z_positions[p.ImagePositionPatient[2]] = f_path

    print('Extracting masks...')
    start_time = datetime.datetime.now()
    totalsegmentator(SCAN_DIR, OUTPUT_DIR, fast=True)
    print(f'Elapsed: {datetime.datetime.now() - start_time}')

    print('Finding Z-position L3 image...')
    mask_file = os.path.join(OUTPUT_DIR, MASK_FILE)
    mask_obj = nib.load(mask_file)
    mask = mask_obj.get_fdata()
    affine_transform = mask_obj.affine

    indexes = np.array(np.where(mask == 1))
    index_min = indexes.min(axis=1)
    index_max = indexes.max(axis=1)
    world_min = nib.affines.apply_affine(affine_transform, index_min)
    world_max = nib.affines.apply_affine(affine_transform, index_max)

    z_direction = affine_transform[:3, 2][2]
    z_sign = math.copysign(1, z_direction)
    z_delta = 0.333 * abs(world_max[2] - world_min[2])
    z_l3 = world_max[2] - z_sign * z_delta

    print(f'Min Z: {world_min[2]}, Max Z: {world_max[2]}, Direction Z: {z_direction}, Sign Z: {z_sign}, Delta Z: {z_delta}')
    print(f'Z-position L3 plane: {z_l3}')

    print('Finding DICOM image closest to L3 image Z-position...')
    positions = sorted(z_positions.keys())
    closest_z = 0
    for z1, z2 in zip(positions[:-1], positions[1:]):
        if min(z1, z2) <= z_l3 <= max(z1, z2):
            closest_z = min(z_positions.keys(), key=lambda z: abs(z - z_l3))
            closest_file = z_positions[closest_z]
            print(f'Closest image: {closest_file}')
            break

    if closest_z == 0:
        print('Could not find slice')
        return
    
    print('Displaying true L3 position vs. calculated one...')
    y_min = positions[0]
    y_max = positions[-1]
    y1 = z_l3
    y2 = closest_z
    plt.figure(figsize=(4, 6))
    plt.axhline(y1, color='blue', linestyle='--', label=f'y1 = {y1}')
    plt.axhline(y2, color='red', linestyle='--', label=f'y2 = {y2}')
    plt.ylim(y_min, y_max)
    plt.xlabel('Value')
    plt.ylabel('Z Position (mm)')
    plt.legend()
    plt.title('Horizontal lines at y1 and y2')
    plt.grid(True)
    plt.savefig("plot.png")


if __name__ == '__main__':
    main()