import io
import os
import zipfile
import camelot

def extract_tables_from_pdf(pdf_path, pages="all"):
    # Read the PDF file and extract tables
    tables = camelot.read_pdf(pdf_path, pages=pages)
    print(tables)
    # Display or process extracted tables
    # for i, table in enumerate(tables):
    #     print(f"Table {i + 1}:")
    #     print(table.df)
    #     print("\n")
    return tables

def convert_df_to_csv(df, output_file):
    """
    Convert DataFrame to CSV file.

    Parameters:
    - df: pandas DataFrame
    - output_file: str, path to the output CSV file
    """
    df.to_csv(output_file, index=False)
    print(f"DataFrame successfully converted to CSV: {output_file}")
    return output_file

def create_zip(directory_path):
    # In-memory buffer to store the zip file
    buffer = io.BytesIO()
    list_of_files = os.listdir(directory_path)

    # Create a ZipFile object
    with zipfile.ZipFile(buffer, 'a', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in list_of_files:
            zipf.write(os.path.join(directory_path, file_path) , arcname=file_path)

    # Set the BytesIO buffer's position to the beginning
    buffer.seek(0)

    # Send the zip file as a response
    return buffer

def write_failure_report(output_string):
     # In-memory buffer to store the file content
    buffer = io.BytesIO()

    # Write content to the buffer
    buffer.write(output_string.encode('utf-8'))

    # Set the BytesIO buffer's position to the beginning
    buffer.seek(0)
    return buffer
