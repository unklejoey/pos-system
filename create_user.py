from app import create_app
from app.models import db, User

app = create_app()

with app.app_context():

    users = [
        {
            "username": "perfumeowner",
            "password": "Owner123",
            "role": "admin"
        },
        {
            "username": "cashier1",
            "password": "Cash123",
            "role": "cashier"
        }
    ]

    for data in users:

        existing = User.query.filter_by(username=data["username"]).first()

        if existing:
            print(f"{data['username']} already exists")
            continue

        user = User(
            username=data["username"],
            role=data["role"],
            is_active=True
        )

        user.set_password(data["password"])

        db.session.add(user)

    db.session.commit()

    print("Users created successfully")
