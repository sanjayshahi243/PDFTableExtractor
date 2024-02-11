import io
import os
import zipfile

import camelot
from pandas import DataFrame


def extract_tables_from_pdf(
    pdf_path: str, pages: str = "all"
) -> camelot.core.TableList:
    """
    Extract tables from a PDF file.

    Parameters:
    - pdf_path (str): Path to the PDF file.
    - pages (str, optional): Specific pages or "all" for all pages. Default is "all".

    Returns:
    - camelot.core.TableList: List of tables extracted from the PDF.
    """
    # Read the PDF file and extract tables
    tables = camelot.read_pdf(pdf_path, pages=pages)
    return tables


def convert_df_to_csv(df: DataFrame, output_file: str) -> str:
    """
    Convert DataFrame to CSV file.

    Parameters:
    - df (DataFrame): pandas DataFrame.
    - output_file (str): Path to the output CSV file.

    Returns:
    - str: Path to the converted CSV file.
    """
    df.to_csv(output_file, index=False)
    print(f"DataFrame successfully converted to CSV: {output_file}")
    return output_file


def create_zip(directory_path: str) -> io.BytesIO:
    """
    Create a zip file from the contents of a directory.

    Parameters:
    - directory_path (str): Path to the directory containing files to be zipped.

    Returns:
    - io.BytesIO: In-memory buffer containing the zip file.
    """
    # In-memory buffer to store the zip file
    buffer = io.BytesIO()
    list_of_files = os.listdir(directory_path)

    # Create a ZipFile object
    with zipfile.ZipFile(buffer, "a", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in list_of_files:
            zipf.write(os.path.join(directory_path, file_path), arcname=file_path)

    # Set the BytesIO buffer's position to the beginning
    buffer.seek(0)

    # Return the in-memory buffer
    return buffer


def write_failure_report(output_string: str) -> io.BytesIO:
    """
    Write failure report to an in-memory buffer.

    Parameters:
    - output_string (str): Content of the failure report.

    Returns:
    - io.BytesIO: In-memory buffer containing the failure report.
    """
    # In-memory buffer to store the file content
    buffer = io.BytesIO()

    # Write content to the buffer
    buffer.write(output_string.encode("utf-8"))

    # Set the BytesIO buffer's position to the beginning
    buffer.seek(0)

    # Return the in-memory buffer
    return buffer
