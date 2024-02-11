from multiprocessing.pool import AsyncResult
from celery import shared_task, current_task
from pdfExtractor.models import TaskModel
from pdfExtractor.utils.pdfExtractor import extract_tables_from_pdf, convert_df_to_csv
from pdfExtractor import db

@shared_task(ignore_result=False)
def process_pdf(file_details: dict) -> str:
    """
    Celery task to process a PDF file, extract tables, and update task status in the database.

    Parameters:
    - file_details (dict): Dictionary containing details about the PDF file.

    Returns:
    - str: Message indicating the task completion.
    """
    try:
        task_id = current_task.request.id
        file_path = file_details.get('file_path')
        file_name = file_path.split('.')[0]
        tables_df = extract_tables_from_pdf(file_path)
        for idx, table in enumerate(tables_df):
            convert_df_to_csv(df=table, output_file=f'{file_name}_table_{idx}.csv')
        update_task_model(task_id, **{"status": "COMPLETE", "number_of_files_generated": len(tables_df)})
        return str(file_details.get("upload_folder"))
    except Exception as e:
        print(e)
        update_task_model(task_id, status="FAILED")
        raise

def update_task_model(task_id: str, **kwargs: dict) -> None:
    """
    Update or create a TaskModel instance with the given task_id and key-value pairs.

    Parameters:
    - task_id (str): Celery task ID.
    - kwargs (dict): Key-value pairs to be updated in the TaskModel instance.

    Returns:
    - None
    """
    # Assuming file_path is unique and can be used to identify the corresponding TaskModel row
    task_instance = TaskModel.query.filter_by(task_id=task_id).first()
    if task_instance:
        for key, value in kwargs.items():
            setattr(task_instance, key, value)
    else:
        task_instance = TaskModel(
            task_id=task_id,
            **kwargs
        )
        db.session.add(task_instance)
    db.session.commit()

# def get_celery_task_status(task_id: str) -> str:
#     """
#     Get the status of a Celery task.

#     Parameters:
#     - task_id (str): Celery task ID.

#     Returns:
#     - str: Status of the Celery task.
#     """
#     result = AsyncResult(task_id)
#     return result.status
