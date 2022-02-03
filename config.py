from os import getenv

class Config(object):
    # Used for securely signing the session cookie and can be used for other security-related needs
    SECRET_KEY = getenv("SECRET_KEY") or 'you-will-never-guess'


    MYSQL_HOST = getenv("MYSQL_HOST")
    MYSQL_PORT = int(getenv("MYSQL_PORT"))
    MYSQL_USER = getenv("MYSQL_USER")
    MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
    MYSQL_DB = getenv("MYSQL_DB")

    CLOUDINARY_NAME = getenv("CLOUDINARY_NAME")
    CLOUDINARY_KEY = getenv("CLOUDINARY_KEY")
    CLOUDINARY_SECRET = getenv("CLOUDINARY_SECRET")

