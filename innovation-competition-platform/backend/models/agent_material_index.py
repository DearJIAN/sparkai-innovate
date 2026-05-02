from extensions import db


class AgentMaterialIndex(db.Model):
    __tablename__ = 'agent_material_indexes'

    id = db.Column(db.Integer, primary_key=True)
    source_type = db.Column(db.String(30), nullable=False)
    source_id = db.Column(db.Integer, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('competition_registrations.id'), nullable=True)
    file_hash = db.Column(db.String(64), nullable=True)
    index_path = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='pending')
    error_message = db.Column(db.Text, nullable=True)
    indexed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    project = db.relationship('Project', backref='material_indexes')

    def to_dict(self):
        return {
            'id': self.id,
            'source_type': self.source_type,
            'source_id': self.source_id,
            'project_id': self.project_id,
            'registration_id': self.registration_id,
            'file_hash': self.file_hash,
            'index_path': self.index_path,
            'status': self.status,
            'error_message': self.error_message,
            'indexed_at': self.indexed_at.isoformat() if self.indexed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f'<AgentMaterialIndex {self.source_type}_{self.source_id} {self.status}>'
