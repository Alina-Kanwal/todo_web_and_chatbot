"""
Authentication API routes.
Provides signup, signin, and signout endpoints.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select
from src.models.user import User
from src.services.auth_service import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
)
from src.core.config import get_settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

settings = get_settings()

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

security = HTTPBearer(auto_error=False)


# Request/Response schemas
class SignupRequest(BaseModel):
    """Request schema for user signup."""

    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters")


class SignupResponse(BaseModel):
    """Response schema for user signup."""

    message: str
    user_id: int
    email: str
    access_token: str
    token_type: str = "bearer"


class SigninRequest(BaseModel):
    """Request schema for user signin."""

    email: EmailStr
    password: str


class SigninResponse(BaseModel):
    """Response schema for user signin."""

    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str


class SignoutResponse(BaseModel):
    """Response schema for user signout."""

    message: str


class ErrorResponse(BaseModel):
    """Generic error response."""

    status_code: int
    error_type: str
    message: str


def get_db_session():
    """Get database session. To be replaced with proper dependency injection."""
    # This will be updated when we add database dependency injection
    from sqlmodel import create_engine
    engine = create_engine(settings.database_url)
    with Session(engine) as session:
        yield session


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    Get current authenticated user from JWT token.

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        dict: User payload from token

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input or duplicate email"},
    },
)
async def signup(request: SignupRequest):
    """
    Create a new user account.

    - **email**: Valid email address (unique)
    - **password**: Minimum 8 characters

    Returns JWT token on successful registration.
    """
    # Create database session with SQLite compatibility
    from sqlmodel import create_engine, Session
    from sqlalchemy import text
    
    # For SQLite, we need to enable foreign keys
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    
    engine = create_engine(settings.database_url, connect_args=connect_args)

    with Session(engine) as session:
        try:
            # Check if user already exists
            existing_user = session.exec(
                select(User).where(User.email == request.email)
            ).first()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

            # Create new user
            password_hash = get_password_hash(request.password)
            user = User(
                email=request.email,
                password_hash=password_hash,
            )

            session.add(user)
            session.commit()
            session.refresh(user)

            # Create JWT token
            access_token = create_access_token(
                data={"user_id": user.id, "email": user.email}
            )

            return SignupResponse(
                message="Account created successfully",
                user_id=user.id,
                email=user.email,
                access_token=access_token,
                token_type="bearer",
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )


@router.post(
    "/signin",
    response_model=SigninResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
async def signin(request: SigninRequest):
    """
    Authenticate user and return JWT token.

    - **email**: Registered email address
    - **password**: User password

    Returns JWT token on successful authentication.
    """
    # Create database session with SQLite compatibility
    from sqlmodel import create_engine, Session
    
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    
    engine = create_engine(settings.database_url, connect_args=connect_args)

    with Session(engine) as session:
        try:
            # Find user
            user = session.exec(select(User).where(User.email == request.email)).first()

            if not user or not verify_password(request.password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            # Create JWT token
            access_token = create_access_token(
                data={"user_id": user.id, "email": user.email}
            )

            return SigninResponse(
                access_token=access_token,
                token_type="bearer",
                user_id=user.id,
                email=user.email,
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )


@router.post(
    "/signout",
    response_model=SignoutResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
async def signout(current_user: dict = Depends(get_current_user)):
    """
    Sign out user (client-side token removal).

    Since we use stateless JWT, this is a client-side operation.
    This endpoint is provided for audit logging purposes.
    """
    return SignoutResponse(message="Successfully signed out")


@router.get("/me", response_model=dict)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    """
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
    }
