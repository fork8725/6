from fastapi import FastAPI, Depends, HTTPException, Request, Header
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from pydantic import BaseModel
from typing import Optional, List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Auth settings
SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Database setup (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy models
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")  # 'admin' or 'user'

# Create tables
Base.metadata.create_all(bind=engine)

# Seed an admin user if none exists
with SessionLocal() as db:
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        hashed = pwd_context.hash("admin123")
        admin = User(username="admin", hashed_password=hashed, role="admin")
        db.add(admin)
        db.commit()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schemas
class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ItemRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserRead(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

app = FastAPI()

# Mount static files and set up templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_model=dict)
async def root():
    return {"message": "Hello World"}

# Auth helpers
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> User:
    token = (authorization or "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserRead)
def me(current: User = Depends(get_current_user)):
    return current

# Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# CRUD endpoints
@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    existing = db.query(Item).filter(Item.name == item.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Item with this name already exists")
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items", response_model=List[ItemRead])
def list_items(db: Session = Depends(get_db)):
    return db.query(Item).order_by(Item.id).all()

@app.get("/items/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    other = db.query(Item).filter(Item.name == item.name, Item.id != item_id).first()
    if other:
        raise HTTPException(status_code=400, detail="Another item with this name exists")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return None
