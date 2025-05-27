import os
import pandas as pd

from PIL import Image

DATA_DIR = os.path.join(os.getcwd(), 'mosamatic', 'experiments', 'pytorch_vs_tensorflow')
PT_CSV = 'metrics_PT.csv'
TF_CSV = 'metrics_TF.csv'


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
    pt_data = pd.read_csv(os.path.join(DATA_DIR, PT_CSV), sep=';')
    tf_data = pd.read_csv(os.path.join(DATA_DIR, TF_CSV), sep=';')

    data = {
        'muscle_area': [],
        'muscle_ra': [],
        'vat_area': [],
        'vat_ra': [],
        'sat_area': [],
        'sat_ra': [],
    }

    for column in ['muscle_area', 'muscle_ra', 'vat_area', 'vat_ra', 'sat_area', 'sat_ra']:
        data[column].append((pt_data[column] - tf_data[column]).abs().mean())

    mean_differences = pd.DataFrame(data=data)
    mean_differences.to_excel(os.path.join(DATA_DIR, 'mean_differences.xlsx'))

    data = {
        'file': [],
        'muscle_area': [],
        'muscle_ra': [],
        'vat_area': [],
        'vat_ra': [],
        'sat_area': [],
        'sat_ra': [],
    }

    for (idx1, row1), (idx2, row2) in zip(pt_data.iterrows(), tf_data.iterrows()):
        data['file'].append(row1['file'])
        for column in data.keys():
            if column == 'file':
                continue
            data[column].append((row1[column] - row2[column]))

    differences = pd.DataFrame(data=data)
    differences.to_excel(os.path.join(DATA_DIR, 'differences.xlsx'))

    # create_comparison_pngs()


if __name__ == '__main__':
    main()