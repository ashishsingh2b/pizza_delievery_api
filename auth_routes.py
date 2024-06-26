from fastapi import APIRouter,status, HTTPException,Depends
from database import Session,engine
from schemas import SignUpModel,LoginModel
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

session = Session(bind=engine)

@auth_router.get("/")
async def hello(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    return {"message": "hello Auth"}

@auth_router.post('/signup', response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()

    return new_user


#login routes


@auth_router.post('/login')
async def login(user:LoginModel, Authorize:AuthJWT=Depends()):
    db_user = session.query(User).filter(User.username==user.username).first()

    if db_user and check_password_hash(db_user.password,user.password):
        access_token=Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response= {
            "access": access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid Username Or Password")

@auth_router.get("/refresh")
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Provide a  valid refresh Token")
    
    current_user = Authorize._get_jwt_subject()
    
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access":access_token})


        

