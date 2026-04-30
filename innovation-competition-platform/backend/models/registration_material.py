from extensions import db


class RegistrationMaterial(db.Model):
    __tablename__ = 'registration_materials'

    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('competition_registrations.id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    material_type = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    original_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # 关系
    uploader = db.relationship('User', backref='registration_materials', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'uploader_id': self.uploader_id,
            'material_type': self.material_type,
            'file_name': self.file_name,
            'original_name': self.original_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<RegistrationMaterial {self.original_name}>'
