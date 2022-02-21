class Config(object):
    import os

    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = True
    ENV = "development"
    SECRET_KEY = "random string"
    SECURITY_PASSWORD_SALT = "another random string"
    
    # both recaptcha key is for development only
    RECAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    RECAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    WTF_CSRF_ENABLED = False
    # media path
    IMAGE_COVER_PATH = os.path.join(basedir, "static/img_cover")
    IMAGE_UPLOAD_PATH = os.path.join(basedir, "static/blog_image")

    SQLALCHEMY_DATABASE_URI = (
        "your_database_url"
    )
    SQLALCHEMY_POOL_TIMEOUT = 86400
    SQLALCHEMY_POOL_SIZE = 200
    SQLALCHEMY_POOL_RECYCLE = 100
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ConfigTest(Config):
    TESTING = True
    SQLALCHEMY_POOL_TIMEOUT = None
    SQLALCHEMY_POOL_SIZE = None
    SQLALCHEMY_POOL_RECYCLE = None