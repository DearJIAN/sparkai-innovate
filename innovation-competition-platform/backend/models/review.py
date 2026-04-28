from extensions import db


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    judge_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    innovation_score = db.Column(db.Float, nullable=True)
    feasibility_score = db.Column(db.Float, nullable=True)
    market_score = db.Column(db.Float, nullable=True)
    team_score = db.Column(db.Float, nullable=True)
    business_score = db.Column(db.Float, nullable=True)
    technology_score = db.Column(db.Float, nullable=True)
    presentation_score = db.Column(db.Float, nullable=True)
    total_score = db.Column(db.Float, nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'judge_id': self.judge_id,
            'innovation_score': self.innovation_score,
            'feasibility_score': self.feasibility_score,
            'market_score': self.market_score,
            'team_score': self.team_score,
            'business_score': self.business_score,
            'technology_score': self.technology_score,
            'presentation_score': self.presentation_score,
            'total_score': self.total_score,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Review project={self.project_id} judge={self.judge_id}>'
