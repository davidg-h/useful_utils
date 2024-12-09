import os
import re
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

def sanitize_path(path):
    """
    Sanitize the user-provided path by removing invalid characters.
    """
    # Remove invalid characters like: < > : " / \ | ? *
    sanitized = re.sub(r'[<>:"|?*\']', '', path).strip()
    return sanitized

def merge_two_pdf(pdf1_path, pdf2_path, output_path):
    """
    Merge two PDFs
    
    Parameters:
    - pdf1_path (str): Path to the first PDF file.
    - pdf2_path (str): Path to the second PDF file.
    - output_path (str): Path to the output PDF file.
    """
    pdf_writer = PdfWriter()

    # Read and add the pages of the first PDF
    pdf_reader1 = PdfReader(pdf1_path)
    for page_num in range(len(pdf_reader1.pages)):
        pdf_writer.add_page(pdf_reader1.pages[page_num])

    # Read and add the pages of the second PDF
    pdf_reader2 = PdfReader(pdf2_path)
    for page_num in range(len(pdf_reader2.pages)):
        pdf_writer.add_page(pdf_reader2.pages[page_num])

    # Save the merged PDF to the output path
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Merged PDF saved as: {output_path}")
    

def merge_pdf(subfolder_path, parent_folder_name):
    """
    Merge all PDFs in a subfolder, preserving top-to-bottom order, and name the output
    based on the parent folder.
    
    Parameters:
    - subfolder_path (str): Path to the folder containing PDFs to merge.
    - parent_folder_name (str): Name of the parent folder, used for the output filename.
    """
    pdf_writer = PdfWriter()

    # Get all PDF files in the subfolder, sorted alphabetically
    pdf_files = sorted(
        [f for f in os.listdir(subfolder_path) if f.lower().endswith(".pdf") and "merge" not in f]
    )

    if not pdf_files:
        print(f"No PDF files found in {subfolder_path}.")
        return

    print(f"Merging PDFs in {subfolder_path}: {pdf_files}")

    # Merge PDFs
    for pdf in pdf_files:
        pdf_path = os.path.join(subfolder_path, pdf)
        pdf_reader = PdfReader(pdf_path)
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_num])

    # Save the merged PDF to the same subfolder
    output_path = os.path.join(subfolder_path, f"merge_{parent_folder_name}.pdf")
    with open(output_path, 'wb') as output_file:
        pdf_writer.write(output_file)

    print(f"Merged PDF saved as: {output_path}")

def process_top_level_folder(folder_path):
    """
    Process a top-level folder containing multiple subfolders with PDFs.
    
    Parameters:
    - folder_path (str): Path to the top-level folder containing subfolders.
    """
    # List all subdirectories in the top-level folder
    subfolders = [
        f.path for f in os.scandir(folder_path) if f.is_dir()
    ]

    if not subfolders:
        print(f"No subfolders found in {folder_path}. Treating {folder_path} as top level folder.")
        merge_pdf(folder_path, folder_path.split("/")[-1])
        return

    # Merge PDFs for each subfolder
    for subfolder in subfolders:
        parent_folder_name = os.path.basename(subfolder)
        merge_pdf(subfolder, parent_folder_name)


if __name__ == "__main__":
    print("Choose an option:")
    print("1. Merge exactly two PDFs")
    print("2. Merge all PDFs in subfolders of a top-level folder")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        pdf1_path = sanitize_path(input("Enter the path of the first PDF: "))
        pdf2_path = sanitize_path(input("Enter the path of the second PDF: "))

        if not (os.path.isfile(pdf1_path) and os.path.isfile(pdf2_path)):
            print("Error: One or both PDF files do not exist.")
        else:
            parent_folder = Path(pdf1_path).parent.absolute()
            output_path = parent_folder.joinpath(f"merge_{parent_folder.name}.pdf") 
            merge_two_pdf(pdf1_path, pdf2_path, output_path)

    elif choice == "2":
        folder_path = sanitize_path(input("Enter the top-level folder path: "))

        if not os.path.isdir(folder_path):
            print(f"Error: '{folder_path}' is not a valid directory.")
        else:
            process_top_level_folder(folder_path)

    else:
        print("Invalid choice. Please select 1 or 2. Terminate program.")# Check if the folder path exists
