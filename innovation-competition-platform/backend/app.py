import os
import sys
from flask import Flask, jsonify, send_from_directory
from sqlalchemy import text
from config import config
from extensions import db, migrate, jwt, cors

# 导入所有模型，确保 Flask-Migrate 能识别
from models import (
    User, Competition, CompetitionTrack, CompetitionRegistration,
    RegistrationMember, RegistrationMaterial,
    Project, ProjectMember, ProjectFile, ProjectTask, Review, AiRecord
)


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 注册蓝图
    register_blueprints(app)

    # 注册错误处理
    register_error_handlers(app)

    # 静态文件服务 - 上传文件
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
        return send_from_directory(upload_folder, filename)
    
    # 健康检查
    @app.route('/api/health')
    def health_check():
        health_status = {'status': 'ok', 'message': '服务运行正常'}
        
        # 检查数据库连接
        try:
            db.session.execute(text('SELECT 1'))
            health_status['database'] = 'connected'
        except Exception as e:
            health_status['database'] = 'disconnected'
            health_status['database_error'] = str(e)
            health_status['status'] = 'degraded'
        
        status_code = 200 if health_status['status'] == 'ok' else 503
        return jsonify(health_status), status_code
    
    return app


def register_blueprints(app):
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.project import project_bp
    from routes.member import member_bp
    from routes.file import file_bp
    from routes.team import team_bp
    from routes.material import material_bp
    from routes.task import task_bp
    from routes.review import review_bp
    from routes.dashboard import dashboard_bp
    from routes.ai import ai_bp
    from routes.competition import competition_bp
    from routes.registration import registration_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(member_bp, url_prefix='/api')
    app.register_blueprint(file_bp, url_prefix='/api')
    app.register_blueprint(team_bp, url_prefix='/api/teams')
    app.register_blueprint(material_bp, url_prefix='/api/materials')
    app.register_blueprint(task_bp, url_prefix='/api')
    app.register_blueprint(review_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(competition_bp, url_prefix='/api')
    app.register_blueprint(registration_bp, url_prefix='/api')


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': '接口不存在'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'message': '服务器内部错误'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': '请求参数错误'}), 400


def init_database(app):
    """初始化数据库，创建所有表"""
    with app.app_context():
        try:
            # 测试数据库连接
            db.session.execute(text('SELECT 1'))
            print('✅ 数据库连接成功')
            
            # 创建表
            db.create_all()
            print('✅ 数据库表创建完成')
        except Exception as e:
            print(f'❌ 数据库连接失败: {e}')
            print('请检查:')
            print('  1. MySQL 服务是否已启动')
            print('  2. 数据库 innovation_competition 是否已创建')
            print('  3. 用户名和密码是否正确')
            print('  4. .env 文件中的 DATABASE_URL 配置')
            sys.exit(1)


# 创建应用实例
app = create_app()

if __name__ == '__main__':
    init_database(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
