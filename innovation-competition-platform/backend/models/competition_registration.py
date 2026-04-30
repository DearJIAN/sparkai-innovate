from extensions import db


class CompetitionRegistration(db.Model):
    __tablename__ = 'competition_registrations'

    id = db.Column(db.Integer, primary_key=True)
    competition_id = db.Column(db.Integer, db.ForeignKey('competitions.id'), nullable=False)
    track_id = db.Column(db.Integer, db.ForeignKey('competition_tracks.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
    leader_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    team_name = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(200), nullable=True)
    college = db.Column(db.String(200), nullable=True)
    major = db.Column(db.String(100), nullable=True)
    teacher_name = db.Column(db.String(100), nullable=True)
    teacher_phone = db.Column(db.String(20), nullable=True)
    contact_phone = db.Column(db.String(20), nullable=True)
    contact_email = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='draft')
    remark = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    submitted_at = db.Column(db.DateTime, nullable=True)

    # 关系
    leader = db.relationship('User', backref='registrations', lazy=True)
    members = db.relationship('RegistrationMember', backref='registration', lazy='dynamic', cascade='all, delete-orphan')
    materials = db.relationship('RegistrationMaterial', backref='registration', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'competition_id': self.competition_id,
            'track_id': self.track_id,
            'project_id': self.project_id,
            'leader_id': self.leader_id,
            'team_name': self.team_name,
            'school': self.school,
            'college': self.college,
            'major': self.major,
            'teacher_name': self.teacher_name,
            'teacher_phone': self.teacher_phone,
            'contact_phone': self.contact_phone,
            'contact_email': self.contact_email,
            'status': self.status,
            'remark': self.remark,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }

    def to_detail_dict(self):
        data = self.to_dict()
        data['leader'] = self.leader.to_dict() if self.leader else None
        data['members'] = [m.to_dict() for m in self.members]
        data['materials'] = [m.to_dict() for m in self.materials]
        return data

    def __repr__(self):
        return f'<CompetitionRegistration {self.team_name}>'
