from enum import Enum

class UserRole(str, Enum):
    GUARD = "guard"
    ADMIN = "admin"
    AUDITOR = "auditor"

class VisitStatus(str, Enum):
    ACTIVE = "active"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"

class AuditEventType(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    CREATE_USER = "create_user"
    REGISTER_VISITOR = "register_visitor"
    CHECK_IN = "check_in"
    CHECK_OUT = "check_out"
    SEARCH_VISITOR = "search_visitor"
    VIEW_REPORT = "view_report"
    VERIFY_AUDIT_CHAIN = "verify_audit_chain"
    RETENTION_DELETE = "retention_delete"