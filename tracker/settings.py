import os

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
IMAGE_UPLOADS = '/home/ubuntu/environment/tracker/static/uploads/img'
ALLOWED_IMAGE_EXTENSIONS = ['PNG', 'JPG', 'JEPG']
MAX_CONTENT_LENGTH = 16 * 1024 * 1024