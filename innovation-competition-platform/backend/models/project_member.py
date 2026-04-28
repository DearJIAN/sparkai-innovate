from extensions import db


class ProjectMember(db.Model):
    __tablename__ = 'project_members'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    member_name = db.Column(db.String(50), nullable=False)
    role_in_project = db.Column(db.String(50), nullable=True)
    responsibility = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # 关系
    user = db.relationship('User', backref='project_memberships')

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'member_name': self.member_name,
            'role_in_project': self.role_in_project,
            'responsibility': self.responsibility,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<ProjectMember {self.member_name}>'
