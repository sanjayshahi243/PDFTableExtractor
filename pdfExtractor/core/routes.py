import os
import time

from flask import Blueprint, send_file
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage

from pdfExtractor.core.tasks import process_pdf, update_task_model
from pdfExtractor.models import TaskModel
from pdfExtractor.utils.pdfExtractor import create_zip, write_failure_report

core_bp = Blueprint("core_bp", __name__)
api = Api(core_bp)

upload_parser = api.parser()
upload_parser.add_argument("file", location="files", type=FileStorage, required=True)


@api.route("/result/<id>")
class Result(Resource):
    def get(self, id: str) -> dict:
        """
        Get the result of a Celery task.

        Parameters:
        - id (str): Celery task ID.

        Returns:
        - dict: Result information.
        """
        task_instance = TaskModel.query.filter_by(task_id=id).first()
        if not task_instance:
            return {"message": "Invalid task id"}
        if task_instance.status == "COMPLETE":
            if not task_instance.number_of_files_generated:
                return {
                    "task_id": task_instance.task_id,
                    "status": task_instance.status,
                    "message": "No tables to extract",
                    "input_file": str(
                        os.path.join(
                            task_instance.upload_directory, task_instance.file_name
                        )
                    ),
                }
            buffer = create_zip(task_instance.upload_directory)
            return send_file(
                buffer,
                download_name=f"{task_instance.upload_directory}.zip",
                as_attachment=True,
            )
        elif task_instance.status == "FAILED":
            buffer = write_failure_report(str(task_instance.info))
            return send_file(
                buffer, download_name=f"{task_instance.task_id}.txt", as_attachment=True
            )
        else:
            return {"task_id": task_instance.task_id, "status": task_instance.status}


@api.route("/upload/pdf/")
@api.expect(upload_parser)
class PDFUpload(Resource):
    def post(self) -> dict:
        """
        Handle the PDF upload API endpoint.

        Returns:
        - dict: Upload response.
        """
        args = upload_parser.parse_args()
        uploaded_file = args["file"]
        if not uploaded_file.filename.split(".")[1] == "pdf":
            return {"message": "Only pdf files allowed"}, 400
        upload_folder = "media/{}_{}".format(
            hex(int(time.time())), uploaded_file.filename.split(".")[0]
        )
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)

        # Pass the file path to the Celery task for processing
        result = process_pdf.delay(
            {"upload_folder": upload_folder, "file_path": file_path}
        )

        create_task = {
            "status": result.status,
            "file_name": uploaded_file.filename,
            "upload_directory": upload_folder,
        }
        update_task_model(result.id, **create_task)

        return {
            "message": "File uploaded successfully",
            "filename": uploaded_file.filename,
            "result_id": result.id,
        }
