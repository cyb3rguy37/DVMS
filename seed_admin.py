from app.db.database import SessionLocal
from app.db.models import User, UserRole
from app.core.security import hash_password

db = SessionLocal()
existing_admin = db.query(User).filter(User.username == "admin").first()

if existing_admin:
    print("Admin user already exists.")
    
else:
    admin = User(
        username="admin",
        password_hash=hash_password("AdminPass123!"),
        role=UserRole.ADMIN,
        is_active=True
    )

    db.add(admin)
    db.commit()

    print("Admin user created successfully.")

db.close()