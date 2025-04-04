# Mosamatic
Web tool for body composition analysis from Maastricht University Medical Center (The Netherlands)


# Development process
- Test app in developer mode (run.bat and run.bat --test)
- Build Docker app (build.bat)
- Run app in Docker mode (run.bat --docker)


# To-do
- Directory upload
- Remove TensorFlow task + package requirements.txt
- Update user manual WordPress
- Automatic slice selection

[x] PyTorch model


# Uploading data
There are different file upload scenario's:
(1) Uploading non-imaging files, e.g., PyTorch model files
(2) Uploading imaging files, where we have the following possibilities:
    (2.1) One image per patient, e.g., L3 or T4 images
    (2.2) One scan or series per patient

Before you upload files you need to specify whether these files should be treated as a single fileset
or as multiple filesets. If you de-select "single fileset", then each file will be added to its own
fileset. Is that what I want? No, files must be grouped into sets that form a fileset. How you group
the files is dependent on the type of data. For example, DICOM files can be grouped by Series Instance UID.