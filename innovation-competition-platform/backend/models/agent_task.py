from extensions import db


class AgentTask(db.Model):
    __tablename__ = 'agent_tasks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('competition_registrations.id'), nullable=True)
    capability = db.Column(db.String(50), nullable=False)
    input_params = db.Column(db.Text, nullable=True)
    result = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship('User', backref='agent_tasks')
    project = db.relationship('Project', backref='agent_tasks')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'registration_id': self.registration_id,
            'capability': self.capability,
            'input_params': self.input_params,
            'result': self.result,
            'status': self.status,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }

    def __repr__(self):
        return f'<AgentTask {self.id} {self.capability}>'
