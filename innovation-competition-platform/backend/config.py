import os
from datetime import timedelta
from dotenv import load_dotenv

# 加载 .env 文件
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def _split_env_list(value, default=''):
    raw = os.environ.get(value, default)
    return [item.strip() for item in raw.split(',') if item.strip()]


class Config:
    # Flask 基础配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:123456@localhost:3306/innovation_competition?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 连接池配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
    
    # JWT 配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    
    # 文件上传配置
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024 * 1024  # 最大 4GB
    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'gif', 'bmp',  # 图片
        'doc', 'docx',  # Word
        'ppt', 'pptx',  # PPT
        'pdf',  # PDF
        'mp4', 'avi', 'mov', 'wmv', 'mkv',  # 视频
        'zip', 'rar', '7z'  # 压缩包
    }

    # 部署与跨域配置
    CORS_ORIGINS = _split_env_list('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173')
    TRUST_PROXY = os.environ.get('TRUST_PROXY', '0').lower() in ('1', 'true', 'yes', 'on')
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
