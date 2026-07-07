from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    UPLOAD_FOLDER = "static/uploads"
    SECRET_KEY = os.getenv("SECRET_KEY")