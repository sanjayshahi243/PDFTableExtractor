from celery import shared_task
from pdfExtractor.utils.pdfExtractor import extract_tables_from_pdf, convert_df_to_csv

@shared_task(ignore_result=False)
def process_pdf(file_details: dict) -> str:
    file_path = file_details.get('file_path')
    file_name = file_path.split('.')[0]
    tables_df = extract_tables_from_pdf(file_path)
    for idx, table in enumerate(tables_df):
        convert_df_to_csv(df=table, output_file=f'{file_name}_table_{idx}.csv')
    return str(file_details.get("upload_folder"))

