#test models
from app.db.models import (
    User,
    Visitor,
    Visit,
    AuditLog,
    ConsentRecord,
    RetentionPolicy,
)

print("Models imported successfully")

print(User.__tablename__)
print(Visitor.__tablename__)
print(Visit.__tablename__)
print(AuditLog.__tablename__)
print(ConsentRecord.__tablename__)
print(RetentionPolicy.__tablename__)