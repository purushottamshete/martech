from fastapi import APIRouter, Request, HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from schema import EmailSchema
import logging
import settings
from models import User as UserModel
from jose import JWTError, jwt
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import db
logger = logging.getLogger(__name__)

router = APIRouter()

email_conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USERNAME,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=settings.EMAIL_PASSWORD,
    MAIL_SSL_TLS=True,
    MAIL_STARTTLS=True,
    USE_CREDENTIALS=True
)

async def send_email(email: list, user: UserModel):
    email_token_data = { "sub": user.email }
    email_verification_token = jwt.encode(email_token_data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    html_template=f"""
    <!DOCTYPE html>
    <html>
        <head></head>
        <body>
            <div>
                <h3> Martech Account Verification </h3>
                <br>
                <p>Thanks for choosing Martech, please click on the button below to verify your account</p>
                <a href="http://localhost:8000/verification/?token={email_verification_token}">Verify Email</a>
            </div>
        </body>
    </html>
    """
    message = MessageSchema(
        subject="Martech Email Verification",
        recipients=email,
        body=html_template,
        subtype="html"
    )
    fm = FastMail(email_conf)
    await fm.send_message(message=message)
    
async def verify_email_token(token: str):
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise token_exception
        db_user = db.session.query(UserModel).filter(UserModel.email == email).first()
        return db_user
    
    except JWTError:
        raise token_exception
    
@router.get('/verification', response_class=JSONResponse)
async def email_verification(request: Request, token: str):
    user = await verify_email_token(token=token)
    if user and not user.is_active:
        user.is_active = True
        db.session.commit()
        db.session.refresh(user)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=f"Email: {user.email} Verified Successfully"
        )
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"},
    )