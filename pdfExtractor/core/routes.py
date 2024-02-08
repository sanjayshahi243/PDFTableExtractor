import os
from flask import Blueprint
from flask_restx import Api, Resource
from werkzeug.datastructures import FileStorage

from pdfExtractor.utils.pdfExtractor import convert_df_to_csv, extract_tables_from_pdf

# from pdfExtractor.utils.base_renderer import CustomRenderer

core_bp = Blueprint("core_bp", __name__)

api = Api(core_bp)

# api.representations['application/json'] = CustomRenderer()

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/upload/pdf/')
@api.expect(upload_parser)
class PDFUpload(Resource):
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        # url = do_something_with_file(uploaded_file)
        # Save the uploaded file to a specific folder (adjust the path as needed)
        upload_folder = 'media'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        file_path = os.path.join(upload_folder, uploaded_file.filename)
        uploaded_file.save(file_path)
        tables_df = extract_tables_from_pdf(file_path)
        for idx, table in enumerate(tables_df):
            convert_df_to_csv(df=table, output_file=f'{file_path}_table_{idx}.csv'.format(file_path, idx))

        return {'message': 'File uploaded successfully', 'filename': uploaded_file.filename}
