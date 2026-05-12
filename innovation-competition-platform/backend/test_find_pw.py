import sys
sys.path.insert(0, '.')
from app import create_app
from werkzeug.security import check_password_hash
app = create_app()
with app.app_context():
    from models import User
    u = User.query.get(2)
    print(f'Username: {u.username}')
    for pw in ['123456', 'password', 'student1', 'admin123', 'test123', 'student']:
        if check_password_hash(u.password_hash, pw):
            print(f'FOUND PASSWORD: {pw}')
            break
    else:
        print('No common password matched')