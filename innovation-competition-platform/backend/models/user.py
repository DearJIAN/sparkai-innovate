from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    real_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='student')
    college = db.Column(db.String(100), nullable=True)
    major = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # 关系
    projects = db.relationship('Project', backref='leader', lazy='dynamic',
                               foreign_keys='Project.leader_id')
    teacher_projects = db.relationship('Project', backref='teacher', lazy='dynamic',
                                       foreign_keys='Project.teacher_id')
    reviews = db.relationship('Review', backref='judge', lazy='dynamic',
                              foreign_keys='Review.judge_id')
    tasks = db.relationship('ProjectTask', backref='assignee', lazy='dynamic',
                            foreign_keys='ProjectTask.assignee_id')
    ai_records = db.relationship('AiRecord', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_judge(self):
        return self.role == 'judge'

    def is_student(self):
        return self.role == 'student'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'real_name': self.real_name,
            'phone': self.phone,
            'college': self.college,
            'major': self.major,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<User {self.username}>'
