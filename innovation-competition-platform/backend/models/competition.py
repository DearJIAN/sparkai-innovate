from extensions import db


class Competition(db.Model):
    __tablename__ = 'competitions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    organizer = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    level = db.Column(db.String(20), nullable=True)
    registration_start = db.Column(db.DateTime, nullable=True)
    registration_end = db.Column(db.DateTime, nullable=True)
    competition_start = db.Column(db.DateTime, nullable=True)
    competition_end = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='draft')
    poster_url = db.Column(db.String(500), nullable=True)
    tags = db.Column(db.String(500), nullable=True)
    target_audience = db.Column(db.String(500), nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    awards = db.Column(db.Text, nullable=True)
    schedule = db.Column(db.Text, nullable=True)
    view_count = db.Column(db.Integer, default=0)
    registration_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # 关系
    projects = db.relationship('Project', backref='competition', lazy='dynamic')
    tracks = db.relationship('CompetitionTrack', backref='competition', lazy='dynamic', cascade='all, delete-orphan')
    registrations = db.relationship('CompetitionRegistration', backref='competition', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'organizer': self.organizer,
            'category': self.category,
            'level': self.level,
            'registration_start': self.registration_start.isoformat() if self.registration_start else None,
            'registration_end': self.registration_end.isoformat() if self.registration_end else None,
            'competition_start': self.competition_start.isoformat() if self.competition_start else None,
            'competition_end': self.competition_end.isoformat() if self.competition_end else None,
            'status': self.status,
            'poster_url': self.poster_url,
            'tags': self.tags.split(',') if self.tags else [],
            'target_audience': self.target_audience,
            'requirements': self.requirements,
            'awards': self.awards,
            'schedule': self.schedule,
            'view_count': self.view_count,
            'registration_count': self.registration_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Competition {self.name}>'
