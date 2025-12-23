import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "dev-key-change-this-in-prod"
    )

    # Main Application DB (Users, Courses, etc.)
    # This creates 'lms.db' in the backend/ folder
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "sqlite:///" + os.path.join(basedir, "../lms.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_ALGORITHM = "HS256"

    # Path to the sample database used by the RA executor (bank/test DBs)
    BANK_DB = os.environ.get("BANK_DB") or os.path.join(basedir, "../bank.db")
