from extensions import db
from datetime import datetime


class MaterialEvaluation(db.Model):
    __tablename__ = 'material_evaluations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    evaluation_type = db.Column(db.String(20), nullable=False, comment='ppt / report')
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, default=0)
    page_count = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='uploaded', comment='uploaded / analyzing / completed / failed')
    progress = db.Column(db.Integer, default=0)

    total_score = db.Column(db.Integer, default=0)
    level = db.Column(db.String(20), default='')
    core_comment = db.Column(db.Text, default='')
    dimension_scores_json = db.Column(db.Text, default='[]')
    advantages_json = db.Column(db.Text, default='[]')
    problems_json = db.Column(db.Text, default='[]')
    suggestions_json = db.Column(db.Text, default='[]')
    next_actions_json = db.Column(db.Text, default='[]')
    keyword_hits = db.Column(db.Integer, default=0)

    pdf_path = db.Column(db.String(500), default='')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref=db.backref('material_evaluations', lazy='dynamic'))

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'user_id': self.user_id,
            'evaluation_type': self.evaluation_type,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'page_count': self.page_count,
            'status': self.status,
            'progress': self.progress,
            'total_score': self.total_score,
            'level': self.level,
            'core_comment': self.core_comment,
            'dimension_scores': json.loads(self.dimension_scores_json) if self.dimension_scores_json else [],
            'advantages': json.loads(self.advantages_json) if self.advantages_json else [],
            'problems': json.loads(self.problems_json) if self.problems_json else [],
            'suggestions': json.loads(self.suggestions_json) if self.suggestions_json else [],
            'next_actions': json.loads(self.next_actions_json) if self.next_actions_json else [],
            'keyword_hits': self.keyword_hits,
            'pdf_path': self.pdf_path,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }