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
