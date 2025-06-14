import zipfile
import os

source_folder = '.'  # Current folder (not "ava_olo" inside it!)
output_zip = '../ava_olo_deploy.zip'  # Goes one level up

excluded_dirs = {'venv', '.git', '__pycache__'}

def should_exclude(path):
    return any(excluded in path.split(os.sep) for excluded in excluded_dirs)

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_folder):
        if should_exclude(root):
            continue
        for file in files:
            filepath = os.path.join(root, file)
            if should_exclude(filepath):
                continue
            arcname = os.path.relpath(filepath, start=source_folder).replace(os.path.sep, '/')
            zipf.write(filepath, arcname)

print(f"✅ Zip created successfully: {output_zip}")
