import os
import time
from flask import Blueprint
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage
from pdfExtractor.core.tasks import process_pdf

# from pdfExtractor.utils.pdfExtractor import convert_df_to_csv, extract_tables_from_pdf
from celery.result import AsyncResult

# from pdfExtractor.utils.base_renderer import CustomRenderer

core_bp = Blueprint("core_bp", __name__)

api = Api(core_bp)

# api.representations['application/json'] = CustomRenderer()

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

@api.route("/result/<id>")
class Result(Resource):
    def get(self, id: str) -> dict[str, object]:
        result = AsyncResult(id)
        return {
            "ready": result.ready(),
            "successful": result.successful(),
            "value": result.result if result.ready() else None,
        }

@api.route('/upload/pdf/')
@api.expect(upload_parser)
class PDFUpload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        if not uploaded_file.filename.split('.')[1] == "pdf":
            return {"message": "Only pdf files allowed"}, 400
        upload_folder = 'media/{}_{}'.format(hex(int(time.time())), uploaded_file.filename.split('.')[0])
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)
        # tables_df = extract_tables_from_pdf(file_path)
        # for idx, table in enumerate(tables_df):
        #     convert_df_to_csv(df=table, output_file=f'{file_path}_table_{idx}.csv'.format(file_path, idx))
        # Pass the file path to the Celery task for processing
        result = process_pdf.delay(file_path)

        return {
            'message': 'File uploaded successfully',
            'filename': uploaded_file.filename,
            "result_id": result.id
        }