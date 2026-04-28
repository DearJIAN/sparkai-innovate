import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models.user import User


def seed_users():
    app = create_app()

    with app.app_context():
        default_users = [
            {
                'username': 'admin',
                'password': 'admin123',
                'role': 'admin',
                'real_name': '管理员',
                'email': 'admin@example.com'
            },
            {
                'username': 'student',
                'password': 'student123',
                'role': 'student',
                'real_name': '学生',
                'email': 'student@example.com'
            },
            {
                'username': 'teacher',
                'password': 'teacher123',
                'role': 'teacher',
                'real_name': '指导老师',
                'email': 'teacher@example.com'
            },
            {
                'username': 'judge',
                'password': 'judge123',
                'role': 'judge',
                'real_name': '评委',
                'email': 'judge@example.com'
            }
        ]

        created_count = 0
        skipped_count = 0

        for user_data in default_users:
            existing = User.query.filter_by(username=user_data['username']).first()
            if existing:
                print(f'  ⚠️  用户 {user_data["username"]} 已存在，跳过')
                skipped_count += 1
                continue

            user = User(
                username=user_data['username'],
                email=user_data.get('email'),
                role=user_data['role'],
                real_name=user_data.get('real_name')
            )
            user.set_password(user_data['password'])

            db.session.add(user)
            created_count += 1
            print(f'  ✅  创建用户: {user_data["username"]} / 角色: {user_data["role"]}')

        db.session.commit()

        print()
        print(f'完成！创建 {created_count} 个用户，跳过 {skipped_count} 个已存在用户')
        print()
        print('默认账号信息：')
        print('  admin     / admin123     (管理员)')
        print('  student   / student123   (学生)')
        print('  teacher   / teacher123   (指导老师)')
        print('  judge     / judge123     (评委)')


if __name__ == '__main__':
    seed_users()
