import streamlit as st
import os
import shutil
import subprocess
from datetime import datetime

# Function to process the uploaded file
def process_file(uploaded_file):

    bytes_data = uploaded_file.read()

    date_str = datetime.now().strftime("%Y_%m_%d")

    # Create a temporary directory to extract files
    temp_dir = os.path.join(os.getcwd(), "temp_dir")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    print("Iniciando o processo de unzip recursivo de arquivos")

    # Extract all zip and rar files in the uploaded file recursively
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.endswith((".zip", ".rar")):
                file_path = os.path.join(root, file)
                parent_path = os.path.dirname(file_path)
                print(f"Extracting {file_path} to {parent_path}")
                if file.endswith(".zip"):
                    arguments = ["-bso0", "-bsp0", "e", f'"{file_path}"',
                                 f'-o"{os.path.join(parent_path, os.path.splitext(file)[0])}"']
                elif file.endswith(".rar"):
                    arguments = ["-bso0", "-bsp0", "x", f'"{file_path}"',
                                 f'-o"{os.path.join(parent_path, os.path.splitext(file)[0])}"']
                ex = subprocess.run(['C:\Program Files\7-Zip\7z.exe'] + arguments, capture_output=True, text=True)
                if ex.returncode == 0:
                    print(f"Extração bem sucedida, deletando {file_path}")
                    os.remove(file_path)
                    shutil.rmtree(os.path.join(parent_path, os.path.splitext(file)[0]), ignore_errors=True)
                    # Remove all pdf files in the extracted directory
                    pdf_path = os.path.join(parent_path, os.path.splitext(file)[0], "*.pdf")
                    shutil.rmtree(pdf_path, ignore_errors=True)

    # Delete specific files with extensions .rem, .xyz, .kev
    print("Iniciando o processo de delete de arquivos específicos")
    for ext in [".rem", ".xyz", ".kev"]:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith(ext):
                    os.remove(os.path.join(root, file))
    print("Fim do processo de deleção de arquivos específicos")

    # Move files to their respective folders
    print("Iniciando o processo de movimentação de arquivos para suas respectivas pastas")
    for root, dirs, files in os.walk(temp_dir):
        print(f"Root: {root}", f"Dirs: {dirs}", f"Files: {files}", sep="\n")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            for file in os.listdir(root):
                file_path = os.path.join(root, file)
                if dir == os.path.splitext(file)[0]:
                    shutil.move(file_path, dir_path)
    print("Fim do processo de movimentação de arquivos para suas respectivas pastas")

    # Rename files with special characters in their names
    print("Inicio do processo de renomeação de arquivos")
    for root, dirs, files in os.walk(temp_dir):
        print('ja foi')
        print( dirs, files)
        for file in files:
            print(file)
            if any(ext in file for ext in [".log", " ", "{", "[", "]", "-", ";", ",", "$"]):
                new_name = file.replace(" ", "_").replace("{", "_").replace("[", "_").replace("]", "_")\
                .replace("-","_").replace(";", "_").replace(",", "_").replace("$", "_")
            os.rename(os.path.join(root, file), os.path.join(root, new_name))
            print("Fim do processo de renomeação de arquivos")

            # Zip the processed directory
            print("Inicio do processo de zip da pasta tratada...")
    for root, dirs, files in os.walk(temp_dir):
        for dir in dirs:
            zip_file_name = f"logs_{dir}_{date_str}.zip"
            shutil.make_archive(os.path.join(root, zip_file_name), 'zip', os.path.join(root, dir))
            print("Fim do processo de zip da pasta tratada")


                    #return the zip file to the user
            print("Iniciando o processo de retorno do arquivo zip para o usuário")
            with open(os.path.join(root, zip_file_name), "rb") as f:
                bytes = f.read()
                st.download_button(
                    label="Download",
                    data=bytes,
                    file_name=zip_file_name,
                    mime="application/zip",
                )
            # Remove the temporary directory
            shutil.rmtree(temp_dir)





uploaded_file = st.file_uploader("Drag and drop a file here", type=["zip", "rar"])
zip_file_path = None
if uploaded_file is not None:
    zip_file_path = process_file(uploaded_file)

if zip_file_path:
    st.download_button(label="Download", data=zip_file_path, file_name=uploaded_file.name+".zip")
else:
    st.write("No file uploaded")