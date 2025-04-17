import os
import nibabel as nib
import datetime
import torch
import numpy as np

from totalsegmentator.python_api import totalsegmentator

SCAN_DIR = 'D:\\Mosamatic\\AutomaticSliceSelection\\scans\\scan1'
OUTPUT_DIR = 'D:\\Mosamatic\\AutomaticSliceSelection\\output'
OUTPUT_DIR_GPU = 'D:\\Mosamatic\\AutomaticSliceSelection\\output_gpu'
MASK_FILE = 'vertebrae_L3.nii.gz'
FAST = True


def main():
    if torch.cuda.is_available():
        
        output_dir = None
        
        # if FAST:            
        #     start_time = datetime.datetime.now()
        #     totalsegmentator(SCAN_DIR, OUTPUT_DIR, fast=True)
        #     print(f'Elapsed: {datetime.datetime.now() - start_time}')
        # else:
        #     start_time = datetime.datetime.now()
        #     totalsegmentator(SCAN_DIR, OUTPUT_DIR_GPU, fast=False)
        #     print(f'Elapsed: {datetime.datetime.now() - start_time}')

        if FAST:
            output_dir = OUTPUT_DIR
        else:
            output_dir = OUTPUT_DIR_GPU
        
        mask_file = os.path.join(output_dir, MASK_FILE)
        mask_obj = nib.load(mask_file)
        mask = mask_obj.get_fdata()
        affine_transform = mask_obj.affine

        indexes = np.array(np.where(mask == 1))
        index_min = indexes.min(axis=1)
        index_max = indexes.max(axis=1)
        world_min = nib.affines.apply_affine(affine_transform, index_min)
        world_max = nib.affines.apply_affine(affine_transform, index_max)

        print(f'world_min: {world_min}, world_max: {world_max}')

        print(f'Min Z: {world_min[2]}, Max Z: {world_max[2]}')

    else:
        print('GPU not available')


if __name__ == '__main__':
    main()