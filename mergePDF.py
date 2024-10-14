import os
from PyPDF2 import PdfReader, PdfWriter

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
        [f for f in os.listdir(subfolder_path) if f.lower().endswith(".pdf")]
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
        print(f"No subfolders found in {folder_path}.")
        return

    # Merge PDFs for each subfolder
    for subfolder in subfolders:
        parent_folder_name = os.path.basename(subfolder)
        merge_pdf(subfolder, parent_folder_name)

if __name__ == "__main__":
    # Input: Top-level folder path containing subfolders with PDFs
    folder_path = "/home/sunraku/code/usefull_utils/pdfs" #input("Enter the top-level folder path: ").strip()

    # Check if the folder path exists
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
    else:
        # Process the top-level folder
        process_top_level_folder(folder_path)
