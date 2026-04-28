from extensions import db


class AiRecord(db.Model):
    __tablename__ = 'ai_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    type = db.Column(db.String(50), nullable=False)
    prompt = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'type': self.type,
            'prompt': self.prompt,
            'result': self.result,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<AiRecord {self.type}>'
