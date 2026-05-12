import sys
sys.path.insert(0, '.')
from app import create_app
from werkzeug.security import generate_password_hash
app = create_app()
with app.app_context():
    from models import User
    from extensions import db
    u = User.query.get(2)
    if u:
        u.password_hash = generate_password_hash('123456')
        db.session.commit()
        print(f'Password for {u.username} reset to: 123456')
    else:
        print('User not found')