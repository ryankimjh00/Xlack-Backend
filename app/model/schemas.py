from pydantic import BaseModel, validator
from datetime import datetime
from .crud.authorization import read_authorizations, read_authorization


class UserBase(BaseModel):
    github_id: str
    email: str
    name: str


class UserCreate(UserBase):
    authorization: str

    @validator('authorization')
    async def check_authorization(cls, v):
        auths = await read_authorizations()
        if len(auths) == 0:
            raise ValueError('No authorizations in database.\nMake authorizations FIRST!')

        auth = await read_authorization(name=v)
        if not auth:
            raise ValueError('No such authorization. Please type it again!')

        return auth.name


class User(UserBase):
    user_id: int
    uuid: str

    created_at: datetime

    class Config:
        orm_mode = True


"""

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), autoincrement=True, unique=True, primary_key=True, nullable=False)
    uuid = Column(String(25), unique=True, nullable=False)

    github_id = Column(String(100), unique=True, nullable=True)

    email = Column(String(100), unique=True, nullable=True)
    name = Column(String(100), unique=False, nullable=True)

    # `func.now()` means `TIMESTAMP.NOW()`.
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

    authorization = Column(String(25), ForeignKey('authorizations.name'))

"""


class AuthrizationBase(BaseModel):
    name: str


class Authorization(AuthrizationBase):
    uuid: str
    created_at: datetime

    class Config:
        orm_mode = True


"""

class Authorization(Base):
    __tablename__ = 'authorizations'

    uuid = Column(String(25), unique=True, nullable=False, primary_key=True)
    name = Column(String(25), nullable=False)
    created_at = Column(TIMESTAMP(), nullable=False, default=func.now())

"""