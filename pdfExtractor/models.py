from pdfExtractor import db

class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(60), nullable=False, unique=True)
    file_name = db.Column(db.Text, nullable=False)
    upload_directory = db.Column(db.Text, nullable=False)
    number_of_files_generated = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(25), nullable=False)
    info = db.Column(db.Text, nullable=True)
