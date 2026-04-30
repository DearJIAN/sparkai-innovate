from extensions import db


class CompetitionTrack(db.Model):
    __tablename__ = 'competition_tracks'

    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    team_min = db.Column(db.Integer, default=1)
    team_max = db.Column(db.Integer, default=5)
    material_requirements = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='open')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # 关系
    registrations = db.relationship('CompetitionRegistration', backref='track', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'team_min': self.team_min,
            'team_max': self.team_max,
            'material_requirements': self.material_requirements,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<CompetitionTrack {self.name}>'
