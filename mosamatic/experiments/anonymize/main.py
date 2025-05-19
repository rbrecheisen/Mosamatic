import os
import pydicom

from deid.config import DeidRecipe
from deid.dicom import get_identifiers, replace_identifiers


INPUT_DIR = "D:\\Mosamatic\\AnonymizerPython"
OUTPUT_DIR = "D:\\Mosamatic\\AnonymizerPythonOutput"
RECIPE_FILE = "D:\\Mosamatic\\AnonymizerPython\\deid.dicom"


os.makedirs(OUTPUT_DIR, exist_ok=True)


for filename in os.listdir(INPUT_DIR):
    if not filename.endswith(".dcm"):
        continue

    dicom_path = os.path.join(INPUT_DIR, filename)
    p = pydicom.dcmread(dicom_path)

    identifiers = get_identifiers(p)

    p = replace_identifiers(p, deid=DeidRecipe(RECIPE_FILE))[0]

    output_path = os.path.join(OUTPUT_DIR, filename)
    p.save_as(output_path)

    print(f"Anonymized: {filename}")
