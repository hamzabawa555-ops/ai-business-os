"""Workflow Database Model"""

from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum
import uuid

Base = declarative_base()

class WorkflowStatus(str, enum.Enum):
    """Workflow status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class TriggerType(str, enum.Enum):
    """Workflow trigger type enumeration"""
    MANUAL = "manual"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"
    API = "api"
    EVENT = "event"

class Workflow(Base):
    """Workflow database model"""
    __tablename__ = "workflows"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.DRAFT, nullable=False)
    trigger_type = Column(Enum(TriggerType), nullable=False)
    trigger_config = Column(JSON, default={}, nullable=False)
    steps = Column(JSON, default=[], nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Workflow {self.name}>"

class WorkflowExecution(Base):
    """Workflow execution history model"""
    __tablename__ = "workflow_executions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    workflow_id = Column(String(36), ForeignKey('workflows.id'), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False, index=True)
    status = Column(String(50), default="running", nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    logs = Column(JSON, default=[], nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<WorkflowExecution {self.id}>"
