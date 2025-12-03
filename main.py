from fastapi import FastAPI, Depends, HTTPException, Request, Header
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Any
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

# Import models
from models import Base, User, RawMaterialTraceRecord, BatchTraceRelation, QualityRiskWarning

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

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class UserRead(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        from_attributes = True

# Section 5.2 schemas
# 5.2.1 RawMaterialTraceRecord
class RawMaterialTraceCreate(BaseModel):
    traceid: str = Field(min_length=1, max_length=32)
    materialbatchno: str = Field(min_length=1, max_length=20)
    tracecode: str = Field(min_length=1, max_length=36)
    supplierid: str = Field(min_length=1, max_length=20)
    purchaseorderid: str = Field(min_length=1, max_length=20)
    incominginspectionid: str = Field(min_length=1, max_length=32)
    receivetime: Optional[datetime] = None
    storagelocation: str = Field(min_length=1, max_length=50)
    usedrecords: List[dict] = Field(default_factory=list)
    remainingqty: float = 0.0
    tracestatus: Literal['In Stock','In Use','Consumed','Scrapped'] = 'In Stock'

class RawMaterialTraceRead(BaseModel):
    traceid: str
    materialbatchno: str
    tracecode: str
    supplierid: str
    purchaseorderid: str
    incominginspectionid: str
    receivetime: datetime
    storagelocation: str
    usedrecords: List[dict]
    remainingqty: float
    tracestatus: str
    class Config:
        from_attributes = True

# 5.2.2 BatchTraceRelation
class BatchTraceRelationCreate(BaseModel):
    relationid: str = Field(min_length=1, max_length=32)
    productbatchno: str = Field(min_length=1, max_length=20)
    producttracecode: str = Field(min_length=1, max_length=36)
    materialtracecode: str = Field(min_length=1, max_length=36)
    equipmentid: str = Field(min_length=1, max_length=20)
    processschemeid: str = Field(min_length=1, max_length=32)
    inspectionpersonid: str = Field(min_length=1, max_length=20)
    inspectiontime: Optional[datetime] = None
    relationstage: str = Field(min_length=1, max_length=30)
    relationstatus: Literal['Valid','Invalid','Pending Confirmation'] = 'Valid'

class BatchTraceRelationRead(BaseModel):
    relationid: str
    productbatchno: str
    producttracecode: str
    materialtracecode: str
    equipmentid: str
    processschemeid: str
    inspectionpersonid: str
    inspectiontime: datetime
    relationstage: str
    relationstatus: str
    class Config:
        from_attributes = True

# 5.2.3 QualityRiskWarning
class QualityRiskWarningCreate(BaseModel):
    warningid: str = Field(min_length=1, max_length=32)
    warningobject: Literal['Raw Material','Semi-Finished Product','Finished Product']
    objectid: str = Field(min_length=1, max_length=32)
    risktype: str = Field(min_length=1, max_length=50)
    risklevel: int = Field(ge=1, le=5, default=3)
    triggercondition: str
    triggertime: Optional[datetime] = None
    handlerid: str = Field(min_length=1, max_length=20)
    handlestatus: Literal['Pending Handling','In Handling','Closed'] = 'Pending Handling'
    handleresult: Optional[str] = None

class QualityRiskWarningRead(BaseModel):
    warningid: str
    warningobject: str
    objectid: str
    risktype: str
    risklevel: int
    triggercondition: str
    triggertime: datetime
    handlerid: str
    handlestatus: str
    handleresult: Optional[str]
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
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> Any:
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

def require_admin(user: Any = Depends(get_current_user)) -> Any:
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

# CRUD for RawMaterialTraceRecord
@app.post("/raw-material-trace", response_model=RawMaterialTraceRead, status_code=201)
def create_raw_material_trace(payload: RawMaterialTraceCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    # uniqueness checks
    if db.query(RawMaterialTraceRecord).filter(RawMaterialTraceRecord.traceid == payload.traceid).first():
        raise HTTPException(status_code=400, detail="traceid already exists")
    if db.query(RawMaterialTraceRecord).filter(RawMaterialTraceRecord.tracecode == payload.tracecode).first():
        raise HTTPException(status_code=400, detail="tracecode already exists")
    receivetime = payload.receivetime or datetime.now(timezone.utc)
    record = RawMaterialTraceRecord(
        traceid=payload.traceid,
        materialbatchno=payload.materialbatchno,
        tracecode=payload.tracecode,
        supplierid=payload.supplierid,
        purchaseorderid=payload.purchaseorderid,
        incominginspectionid=payload.incominginspectionid,
        receivetime=receivetime,
        storagelocation=payload.storagelocation,
        usedrecords=payload.usedrecords,
        remainingqty=payload.remainingqty,
        tracestatus=payload.tracestatus,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get("/raw-material-trace", response_model=List[RawMaterialTraceRead])
def list_raw_material_trace(db: Session = Depends(get_db)):
    return db.query(RawMaterialTraceRecord).order_by(RawMaterialTraceRecord.receivetime.desc()).all()

@app.get("/raw-material-trace/{traceid}", response_model=RawMaterialTraceRead)
def get_raw_material_trace(traceid: str, db: Session = Depends(get_db)):
    record = db.query(RawMaterialTraceRecord).filter(RawMaterialTraceRecord.traceid == traceid).first()
    if not record:
        raise HTTPException(status_code=404, detail="RawMaterialTraceRecord not found")
    return record

@app.delete("/raw-material-trace/{traceid}", status_code=204)
def delete_raw_material_trace(traceid: str, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    record = db.query(RawMaterialTraceRecord).filter(RawMaterialTraceRecord.traceid == traceid).first()
    if not record:
        raise HTTPException(status_code=404, detail="RawMaterialTraceRecord not found")
    db.delete(record)
    db.commit()
    return None

# CRUD for BatchTraceRelation
@app.post("/batch-trace-relations", response_model=BatchTraceRelationRead, status_code=201)
def create_batch_trace_relation(payload: BatchTraceRelationCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.query(BatchTraceRelation).filter(BatchTraceRelation.relationid == payload.relationid).first():
        raise HTTPException(status_code=400, detail="relationid already exists")
    if db.query(BatchTraceRelation).filter(BatchTraceRelation.producttracecode == payload.producttracecode).first():
        raise HTTPException(status_code=400, detail="producttracecode already exists")
    # validate materialtracecode exists in RawMaterialTraceRecord
    if not db.query(RawMaterialTraceRecord).filter(RawMaterialTraceRecord.tracecode == payload.materialtracecode).first():
        raise HTTPException(status_code=400, detail="materialtracecode not found in raw material records")
    inspectiontime = payload.inspectiontime or datetime.now(timezone.utc)
    rel = BatchTraceRelation(
        relationid=payload.relationid,
        productbatchno=payload.productbatchno,
        producttracecode=payload.producttracecode,
        materialtracecode=payload.materialtracecode,
        equipmentid=payload.equipmentid,
        processschemeid=payload.processschemeid,
        inspectionpersonid=payload.inspectionpersonid,
        inspectiontime=inspectiontime,
        relationstage=payload.relationstage,
        relationstatus=payload.relationstatus,
    )
    db.add(rel)
    db.commit()
    db.refresh(rel)
    return rel

@app.get("/batch-trace-relations", response_model=List[BatchTraceRelationRead])
def list_batch_trace_relations(db: Session = Depends(get_db)):
    return db.query(BatchTraceRelation).order_by(BatchTraceRelation.inspectiontime.desc()).all()

@app.get("/batch-trace-relations/{relationid}", response_model=BatchTraceRelationRead)
def get_batch_trace_relation(relationid: str, db: Session = Depends(get_db)):
    rel = db.query(BatchTraceRelation).filter(BatchTraceRelation.relationid == relationid).first()
    if not rel:
        raise HTTPException(status_code=404, detail="BatchTraceRelation not found")
    return rel

@app.delete("/batch-trace-relations/{relationid}", status_code=204)
def delete_batch_trace_relation(relationid: str, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    rel = db.query(BatchTraceRelation).filter(BatchTraceRelation.relationid == relationid).first()
    if not rel:
        raise HTTPException(status_code=404, detail="BatchTraceRelation not found")
    db.delete(rel)
    db.commit()
    return None

# CRUD for QualityRiskWarning
@app.post("/quality-risk-warnings", response_model=QualityRiskWarningRead, status_code=201)
def create_quality_risk_warning(payload: QualityRiskWarningCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.query(QualityRiskWarning).filter(QualityRiskWarning.warningid == payload.warningid).first():
        raise HTTPException(status_code=400, detail="warningid already exists")
    triggertime = payload.triggertime or datetime.now(timezone.utc)
    warn = QualityRiskWarning(
        warningid=payload.warningid,
        warningobject=payload.warningobject,
        objectid=payload.objectid,
        risktype=payload.risktype,
        risklevel=payload.risklevel,
        triggercondition=payload.triggercondition,
        triggertime=triggertime,
        handlerid=payload.handlerid,
        handlestatus=payload.handlestatus,
        handleresult=payload.handleresult,
    )
    db.add(warn)
    db.commit()
    db.refresh(warn)
    return warn

@app.get("/quality-risk-warnings", response_model=List[QualityRiskWarningRead])
def list_quality_risk_warnings(db: Session = Depends(get_db)):
    return db.query(QualityRiskWarning).order_by(QualityRiskWarning.triggertime.desc()).all()

@app.get("/quality-risk-warnings/{warningid}", response_model=QualityRiskWarningRead)
def get_quality_risk_warning(warningid: str, db: Session = Depends(get_db)):
    warn = db.query(QualityRiskWarning).filter(QualityRiskWarning.warningid == warningid).first()
    if not warn:
        raise HTTPException(status_code=404, detail="QualityRiskWarning not found")
    return warn

@app.delete("/quality-risk-warnings/{warningid}", status_code=204)
def delete_quality_risk_warning(warningid: str, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    warn = db.query(QualityRiskWarning).filter(QualityRiskWarning.warningid == warningid).first()
    if not warn:
        raise HTTPException(status_code=404, detail="QualityRiskWarning not found")
    db.delete(warn)
    db.commit()
    return None
