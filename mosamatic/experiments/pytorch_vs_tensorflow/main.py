import os
import pandas as pd

from PIL import Image

DATA_DIR = os.path.join(os.getcwd(), 'mosamatic', 'experiments', 'pytorch_vs_tensorflow')


def create_comparison_pngs():
    dir1 = 'C:\\Users\\r.brecheisen\\Desktop\\pngs\\pytorch'
    dir2 = 'C:\\Users\\r.brecheisen\\Desktop\\pngs\\tensorflow'
    output_dir = 'C:\\Users\\r.brecheisen\\Desktop\\pngs\\pytorch_tensorflow'
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(dir1):
        if filename.lower().endswith('.png'):
            path1 = os.path.join(dir1, filename)
            path2 = os.path.join(dir2, filename)

            if os.path.exists(path2):
                img1 = Image.open(path1)
                img2 = Image.open(path2)

                # Ensure same height
                if img1.height != img2.height:
                    raise ValueError(f"Image heights don't match for {filename}")

                combined_width = img1.width + img2.width
                combined_img = Image.new('RGB', (combined_width, img1.height))
                combined_img.paste(img1, (0, 0))
                combined_img.paste(img2, (img1.width, 0))

                combined_img.save(os.path.join(output_dir, filename))


def main():
    pt_data = pd.read_csv(os.path.join(DATA_DIR, 'metrics_pytorch.csv'), sep=';')
    tf_data = pd.read_csv(os.path.join(DATA_DIR, 'metrics_tensorflow.csv'), sep=';')

    print('Mean differences:')
    for column in ['muscle_area', 'muscle_ra', 'vat_area', 'vat_ra', 'sat_area', 'sat_ra']:
        print('{}:\t\t{}'.format(column, (pt_data[column] - tf_data[column]).abs().mean()))
    print()

    print('Per file differences in muscle area:')
    for (idx1, row1), (idx2, row2) in zip(pt_data.iterrows(), tf_data.iterrows()):
        print('{}: {} (PT) - {} (TF)'.format(row1['file'], row1['muscle_area'], row2['muscle_area']))

    create_comparison_pngs()


if __name__ == '__main__':
    main()