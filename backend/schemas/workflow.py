"""Workflow database schema"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum

class WorkflowStatus(str, Enum):
    """Workflow status"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class TriggerType(str, Enum):
    """Trigger type"""
    MANUAL = "manual"
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"
    API = "api"
    EVENT = "event"

class WorkflowStep(BaseModel):
    """Workflow step"""
    id: str
    name: str
    action_type: str
    config: Dict[str, Any] = {}
    order: int

class WorkflowTrigger(BaseModel):
    """Workflow trigger"""
    type: TriggerType
    config: Dict[str, Any] = {}

class WorkflowBase(BaseModel):
    """Base workflow schema"""
    name: str
    description: Optional[str] = None
    trigger_type: TriggerType
    trigger_config: Dict[str, Any] = {}
    steps: List[WorkflowStep] = []

class WorkflowCreate(WorkflowBase):
    """Workflow creation schema"""
    pass

class WorkflowUpdate(BaseModel):
    """Workflow update schema"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[WorkflowStatus] = None
    trigger_type: Optional[TriggerType] = None
    trigger_config: Optional[Dict[str, Any]] = None
    steps: Optional[List[WorkflowStep]] = None

class WorkflowResponse(WorkflowBase):
    """Workflow response schema"""
    id: str
    user_id: str
    status: WorkflowStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WorkflowExecutionResponse(BaseModel):
    """Workflow execution response schema"""
    id: str
    workflow_id: str
    user_id: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    logs: List[Dict[str, Any]] = []

    class Config:
        from_attributes = True
