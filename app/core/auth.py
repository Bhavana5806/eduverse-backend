"""
Enhanced Authentication and Authorization System for EduVerse AI
JWT-based authentication with role-based access control and security features
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import secrets
import hashlib
from app.core.config import settings
from app.db.database import get_db
from app.db.enhanced_models import User
from sqlalchemy.orm import Session

# Security configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Token types
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"
RESET_TOKEN_TYPE = "reset"

class AuthManager:
    """Centralized authentication and authorization manager"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": ACCESS_TOKEN_TYPE})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": REFRESH_TOKEN_TYPE})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_reset_token(email: str) -> str:
        """Create password reset token"""
        data = {"sub": email, "type": RESET_TOKEN_TYPE}
        expire = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
        data.update({"exp": expire})
        return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def verify_token(token: str, token_type: str = ACCESS_TOKEN_TYPE) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            # Verify token type
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type. Expected {token_type}",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check if token is expired
            if payload.get("exp") and datetime.utcnow().timestamp() > payload["exp"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return payload
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

class UserAuthenticator:
    """User authentication operations"""
    
    @staticmethod
    async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user or not AuthManager.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
    ) -> User:
        """Get current authenticated user"""
        payload = AuthManager.verify_token(credentials.credentials)
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
        """Get current active user"""
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

class RoleBasedAccessControl:
    """Role-based access control manager"""
    
    @staticmethod
    def require_roles(required_roles: list):
        """Decorator to require specific roles"""
        def role_checker(current_user: User = Depends(UserAuthenticator.get_current_active_user)):
            if current_user.role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            return current_user
        return role_checker
    
    @staticmethod
    def require_student(current_user: User = Depends(UserAuthenticator.get_current_active_user)):
        """Require student role"""
        if current_user.role != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Student access required"
            )
        return current_user
    
    @staticmethod
    def require_teacher(current_user: User = Depends(UserAuthenticator.get_current_active_user)):
        """Require teacher role"""
        if current_user.role != "teacher":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Teacher access required"
            )
        return current_user
    
    @staticmethod
    def require_admin(current_user: User = Depends(UserAuthenticator.get_current_active_user)):
        """Require admin role"""
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user
    
    @staticmethod
    def require_mentor(current_user: User = Depends(UserAuthenticator.get_current_active_user)):
        """Require mentor role"""
        if current_user.role != "mentor":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Mentor access required"
            )
        return current_user

class SecurityManager:
    """Security management and monitoring"""
    
    @staticmethod
    def generate_session_id() -> str:
        """Generate unique session ID"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash sensitive data for storage"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength"""
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one number")
        
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain at least one special character")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "strength": "strong" if len(errors) == 0 else "weak"
        }
    
    @staticmethod
    def sanitize_input(input_string: str) -> str:
        """Sanitize user input to prevent injection attacks"""
        # Remove potentially dangerous characters
        dangerous_chars = ["<", ">", "\"", "'", ";", "&", "|", "$", "`", "\\", "/"]
        for char in dangerous_chars:
            input_string = input_string.replace(char, "")
        return input_string.strip()

class OAuthManager:
    """OAuth integration manager"""
    
    @staticmethod
    def generate_oauth_state() -> str:
        """Generate OAuth state parameter"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def verify_oauth_state(state: str, stored_state: str) -> bool:
        """Verify OAuth state parameter"""
        return secrets.compare_digest(state, stored_state)

# Dependency functions for FastAPI
get_current_user = UserAuthenticator.get_current_user
get_current_active_user = UserAuthenticator.get_current_active_user

# Role-based dependencies
get_student = RoleBasedAccessControl.require_student
get_teacher = RoleBasedAccessControl.require_teacher
get_admin = RoleBasedAccessControl.require_admin
get_mentor = RoleBasedAccessControl.require_mentor

# Common role combinations
get_teacher_or_admin = RoleBasedAccessControl.require_roles(["teacher", "admin"])
get_student_or_teacher = RoleBasedAccessControl.require_roles(["student", "teacher"])
get_all_authenticated = RoleBasedAccessControl.require_roles(["student", "teacher", "admin", "mentor"])

class SecurityHeaders:
    """Security headers configuration"""
    
    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """Get security headers for responses"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

class RateLimitManager:
    """Rate limiting for API endpoints"""
    
    def __init__(self):
        self.rate_limits = {}
    
    def check_rate_limit(self, identifier: str, limit: int, window: int) -> bool:
        """
        Check if request is within rate limit
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            limit: Maximum requests allowed
            window: Time window in seconds
        """
        current_time = datetime.utcnow().timestamp()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Remove old requests outside the window
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier]
            if current_time - req_time < window
        ]
        
        # Check if within limit
        if len(self.rate_limits[identifier]) >= limit:
            return False
        
        # Add current request
        self.rate_limits[identifier].append(current_time)
        return True

# Global rate limiter instance
rate_limiter = RateLimitManager()

# Security configuration constants
SECURITY_CONFIG = {
    "MAX_LOGIN_ATTEMPTS": 5,
    "LOCKOUT_DURATION": 30 * 60,  # 30 minutes
    "SESSION_TIMEOUT": 24 * 60 * 60,  # 24 hours
    "PASSWORD_RESET_TIMEOUT": 60 * 60,  # 1 hour
    "CSRF_TOKEN_EXPIRY": 30 * 60,  # 30 minutes
}