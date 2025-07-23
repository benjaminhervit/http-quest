
from dataclasses import dataclass
from app.models import User

@dataclass
class AuthResult:
    success: bool
    user: User | None