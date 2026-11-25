from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, revoke_token
from app.core.rate_limit import rate_limit_login, rate_limit_register
from app.models.entities import User, UserRole
from app.schemas.schemas import Token, LoginRequest, UserRegister, UserResponse
from app.api.deps import get_current_user
from app.services.audit_service import log_audit_event

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token, dependencies=[Depends(rate_limit_login)])
def login(
    req: LoginRequest, 
    request: Request,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == req.email.lower().strip()).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas o usuario no registrado",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Esta cuenta ha sido desactivada temporalmente",
        )
        
    access_token = create_access_token(subject=user.id, role=user.role)
    
    # Audit login
    log_audit_event(
        db=db,
        action="USER_LOGIN",
        entity_name="users",
        entity_id=user.id,
        user_id=user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        role=user.role,
        user_id=user.id,
        full_name=user.full_name
    )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit_register)])
def register(
    user_in: UserRegister, 
    request: Request,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(User.email == user_in.email.lower().strip()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta registrada con este correo electrónico",
        )
        
    # Enforce safe default role
    assigned_role = UserRole.REPORTER.value if user_in.role == "reporter" else UserRole.CITIZEN.value
    
    new_user = User(
        email=user_in.email.lower().strip(),
        password_hash=get_password_hash(user_in.password),
        full_name=user_in.full_name.strip(),
        phone_number=user_in.phone_number,
        role=assigned_role,
        is_active=True,
        is_verified=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log_audit_event(
        db=db,
        action="USER_REGISTER",
        entity_name="users",
        entity_id=new_user.id,
        user_id=new_user.id,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    
    return new_user

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1].strip()
        revoke_token(token)

    log_audit_event(
        db=db,
        action="USER_LOGOUT",
        entity_name="users",
        entity_id=current_user.id,
        user_id=current_user.id,
        ip_address=request.client.host if request.client else None
    )
    return {"message": "Sesión cerrada correctamente y credencial de acceso revocada"}
