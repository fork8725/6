# // filepath: c:\Users\W\Desktop\py\6\models.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, JSON, DECIMAL, CheckConstraint, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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
    role = Column(String(20), nullable=False, default="user")

# 5.2.1 Raw Material Trace Record Table
class RawMaterialTraceRecord(Base):
    __tablename__ = "rawmaterialtracerecord"
    traceid = Column(String(32), primary_key=True, nullable=False, unique=True)
    materialbatchno = Column(String(20), nullable=False)
    tracecode = Column(String(36), nullable=False, unique=True)
    supplierid = Column(String(20), nullable=False)
    purchaseorderid = Column(String(20), nullable=False)
    incominginspectionid = Column(String(32), nullable=False)
    receivetime = Column(TIMESTAMP, nullable=False)
    storagelocation = Column(String(50), nullable=False)
    usedrecords = Column(JSON, nullable=False, default=list)
    remainingqty = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    tracestatus = Column(String(15), nullable=False, default='In Stock')

    __table_args__ = (
        CheckConstraint("tracestatus IN ('In Stock','In Use','Consumed','Scrapped')", name="chk_tracestatus"),
    )

# 5.2.2 Batch Trace Relation Table
class BatchTraceRelation(Base):
    __tablename__ = "batchtracerelation"
    relationid = Column(String(32), primary_key=True, nullable=False, unique=True)
    productbatchno = Column(String(20), nullable=False)
    producttracecode = Column(String(36), nullable=False, unique=True)
    materialtracecode = Column(String(36), ForeignKey("rawmaterialtracerecord.tracecode"), nullable=False)
    equipmentid = Column(String(20), nullable=False)
    processschemeid = Column(String(32), nullable=False)
    inspectionpersonid = Column(String(20), nullable=False)
    inspectiontime = Column(TIMESTAMP, nullable=False)
    relationstage = Column(String(30), nullable=False)
    relationstatus = Column(String(15), nullable=False, default='Valid')

    __table_args__ = (
        CheckConstraint("relationstatus IN ('Valid','Invalid','Pending Confirmation')", name="chk_relationstatus"),
    )

# 5.2.3 Quality Risk Warning Table
class QualityRiskWarning(Base):
    __tablename__ = "qualityriskwarning"
    warningid = Column(String(32), primary_key=True, nullable=False, unique=True)
    warningobject = Column(String(15), nullable=False)
    objectid = Column(String(32), nullable=False)
    risktype = Column(String(50), nullable=False)
    risklevel = Column(Integer, nullable=False, default=3)
    triggercondition = Column(Text, nullable=False)
    triggertime = Column(TIMESTAMP, nullable=False)
    handlerid = Column(String(20), nullable=False)
    handlestatus = Column(String(15), nullable=False, default='Pending Handling')
    handleresult = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("risklevel BETWEEN 1 AND 5", name="chk_risklevel"),
        CheckConstraint("warningobject IN ('Raw Material','Semi-Finished Product','Finished Product')", name="chk_warningobject"),
        CheckConstraint("handlestatus IN ('Pending Handling','In Handling','Closed')", name="chk_handlestatus"),
    )

