from extensions import db


class RegistrationMember(db.Model):
    __tablename__ = 'registration_members'

    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('competition_registrations.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    student_no = db.Column(db.String(50), nullable=True)
    college = db.Column(db.String(200), nullable=True)
    major = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    role_in_team = db.Column(db.String(20), default='member')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'registration_id': self.registration_id,
            'name': self.name,
            'student_no': self.student_no,
            'college': self.college,
            'major': self.major,
            'phone': self.phone,
            'email': self.email,
            'role_in_team': self.role_in_team,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<RegistrationMember {self.name}>'
