"""Workflow Service"""

import logging
from datetime import datetime
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from backend.models.models import Workflow, WorkflowExecution, ExecutionStatus, WorkflowStatus
import json
import time

logger = logging.getLogger(__name__)

class WorkflowService:
    """Workflow Service for managing workflows and executions"""
    
    @staticmethod
    def create_workflow(
        db: Session,
        name: str,
        created_by: str,
        trigger_type: str,
        trigger_config: dict,
        description: Optional[str] = None,
        steps: Optional[List[dict]] = None
    ) -> Tuple[Optional[Workflow], Optional[str]]:
        """Create new workflow"""
        try:
            workflow = Workflow(
                name=name,
                description=description,
                trigger_type=trigger_type,
                trigger_config=trigger_config or {},
                steps=steps or [],
                created_by=created_by
            )
            
            db.add(workflow)
            db.commit()
            db.refresh(workflow)
            
            logger.info(f"Workflow created: {workflow.id} by user {created_by}")
            return workflow, None
        except Exception as e:
            db.rollback()
            logger.error(f"Workflow creation error: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def get_workflow(db: Session, workflow_id: str) -> Optional[Workflow]:
        """Get workflow by ID"""
        try:
            return db.query(Workflow).filter(Workflow.id == workflow_id).first()
        except Exception as e:
            logger.error(f"Get workflow error: {str(e)}")
            return None
    
    @staticmethod
    def get_user_workflows(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Workflow]:
        """Get all workflows for a user"""
        try:
            return db.query(Workflow).filter(
                Workflow.created_by == user_id
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Get user workflows error: {str(e)}")
            return []
    
    @staticmethod
    def update_workflow(
        db: Session,
        workflow_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        trigger_type: Optional[str] = None,
        trigger_config: Optional[dict] = None,
        steps: Optional[List[dict]] = None
    ) -> Tuple[Optional[Workflow], Optional[str]]:
        """Update workflow"""
        try:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                return None, "Workflow not found"
            
            if name:
                workflow.name = name
            if description is not None:
                workflow.description = description
            if status:
                workflow.status = WorkflowStatus(status)
            if trigger_type:
                workflow.trigger_type = trigger_type
            if trigger_config:
                workflow.trigger_config = trigger_config
            if steps:
                workflow.steps = steps
            
            workflow.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(workflow)
            
            logger.info(f"Workflow updated: {workflow_id}")
            return workflow, None
        except Exception as e:
            db.rollback()
            logger.error(f"Workflow update error: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def delete_workflow(db: Session, workflow_id: str) -> Tuple[bool, Optional[str]]:
        """Delete workflow"""
        try:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                return False, "Workflow not found"
            
            db.delete(workflow)
            db.commit()
            
            logger.info(f"Workflow deleted: {workflow_id}")
            return True, None
        except Exception as e:
            db.rollback()
            logger.error(f"Workflow deletion error: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def activate_workflow(db: Session, workflow_id: str) -> Tuple[Optional[Workflow], Optional[str]]:
        """Activate workflow"""
        try:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                return None, "Workflow not found"
            
            workflow.status = WorkflowStatus.ACTIVE
            workflow.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(workflow)
            
            logger.info(f"Workflow activated: {workflow_id}")
            return workflow, None
        except Exception as e:
            db.rollback()
            logger.error(f"Workflow activation error: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def pause_workflow(db: Session, workflow_id: str) -> Tuple[Optional[Workflow], Optional[str]]:
        """Pause workflow"""
        try:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                return None, "Workflow not found"
            
            workflow.status = WorkflowStatus.PAUSED
            workflow.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(workflow)
            
            logger.info(f"Workflow paused: {workflow_id}")
            return workflow, None
        except Exception as e:
            db.rollback()
            logger.error(f"Workflow pause error: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def execute_workflow(db: Session, workflow_id: str) -> Tuple[Optional[WorkflowExecution], Optional[str]]:
        """Execute workflow"""
        try:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                return None, "Workflow not found"
            
            if workflow.status != WorkflowStatus.ACTIVE:
                return None, f"Workflow is {workflow.status}, cannot execute"
            
            # Create execution record
            execution = WorkflowExecution(
                workflow_id=workflow_id,
                status=ExecutionStatus.RUNNING
            )
            
            db.add(execution)
            db.flush()
            
            # Execute steps
            start_time = time.time()
            result = {}
            error = None
            steps_executed = 0
            
            try:
                for idx, step in enumerate(workflow.steps):
                    steps_executed += 1
                    # TODO: Implement actual step execution logic
                    logger.info(f"Executing step {idx + 1} of workflow {workflow_id}")
                    result[f"step_{idx}"] = {"status": "completed"}
                
                execution.status = ExecutionStatus.COMPLETED
                execution.result = result
            except Exception as step_error:
                execution.status = ExecutionStatus.FAILED
                error = str(step_error)
                execution.error = error
                logger.error(f"Workflow execution error: {str(step_error)}")
            
            # Update execution details
            execution_time_ms = int((time.time() - start_time) * 1000)
            execution.completed_at = datetime.utcnow()
            execution.execution_time_ms = execution_time_ms
            execution.steps_executed = steps_executed
            
            # Update workflow
            workflow.last_executed = datetime.utcnow()
            workflow.execution_count += 1
            
            db.commit()
            db.refresh(execution)
            
            logger.info(f"Workflow executed: {workflow_id} in {execution_time_ms}ms")
            return execution, error
        except Exception as e:
            db.rollback()
            logger.error(f"Workflow execution error: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def get_workflow_executions(
        db: Session,
        workflow_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[WorkflowExecution]:
        """Get workflow executions"""
        try:
            return db.query(WorkflowExecution).filter(
                WorkflowExecution.workflow_id == workflow_id
            ).order_by(WorkflowExecution.started_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Get executions error: {str(e)}")
            return []
    
    @staticmethod
    def get_workflow_execution(
        db: Session,
        workflow_id: str,
        execution_id: str
    ) -> Optional[WorkflowExecution]:
        """Get specific workflow execution"""
        try:
            return db.query(WorkflowExecution).filter(
                WorkflowExecution.workflow_id == workflow_id,
                WorkflowExecution.id == execution_id
            ).first()
        except Exception as e:
            logger.error(f"Get execution error: {str(e)}")
            return None
