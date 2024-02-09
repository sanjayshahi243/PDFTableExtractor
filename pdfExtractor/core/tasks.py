from celery import shared_task

@shared_task(ignore_result=False)
def process_pdf(file_path: str) -> str:
    from pdfExtractor.utils.pdfExtractor import extract_tables_from_pdf, convert_df_to_csv
    tables_df = extract_tables_from_pdf(file_path)
    for idx, table in enumerate(tables_df):
        convert_df_to_csv(df=table, output_file=f'{file_path}_table_{idx}.csv')
    return str(file_path)

