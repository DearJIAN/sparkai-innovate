from extensions import db


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    track = db.Column(db.String(50), nullable=True)
    stage = db.Column(db.String(30), default='idea')
    status = db.Column(db.String(30), default='draft')
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=True)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # 关系
    members = db.relationship('ProjectMember', backref='project', lazy='dynamic',
                              cascade='all, delete-orphan')
    files = db.relationship('ProjectFile', backref='project', lazy='dynamic',
                            cascade='all, delete-orphan')
    tasks = db.relationship('ProjectTask', backref='project', lazy='dynamic',
                            cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='project', lazy='dynamic',
                              cascade='all, delete-orphan')
    ai_records = db.relationship('AiRecord', backref='project', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'track': self.track,
            'stage': self.stage,
            'status': self.status,
            'leader_id': self.leader_id,
            'teacher_id': self.teacher_id,
            'competition_id': self.competition_id,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Project {self.name}>'
