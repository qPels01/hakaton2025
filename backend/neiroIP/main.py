from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
import asyncio
import json
from enum import Enum
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import your project management system
from project_system import ProjectManagementSystem, TaskStatus, ProjectStatus

app = FastAPI(
    title="Project Management API",
    description="API для управления проектами и задачами с контролем времени",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration - CONFIGURE THIS!
DATABASE_URL = "postgresql://postgres:user@localhost:5432/project_management"

# Global variable for the system
project_system: Optional[ProjectManagementSystem] = None


# Enums for validation
class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    blocked = "blocked"
    cancelled = "cancelled"


class ProjectStatusEnum(str, Enum):
    planning = "planning"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"
    on_hold = "on_hold"


# Pydantic models for API
class ProjectCreateRequest(BaseModel):
    title: Optional[str] = None
    description: str = Field(..., min_length=10, max_length=1000)
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_phone: Optional[str] = None
    client_company: Optional[str] = None
    client_notes: Optional[str] = None
    priority: int = Field(default=1, ge=1, le=5)

    @field_validator('client_email')
    @classmethod
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Некорректный email адрес')
        return v


class ProjectResponse(BaseModel):
    project: Dict[str, Any]
    timeline: Dict[str, Any]
    team_assignment: Dict[str, Any]
    detailed_tasks: List[Dict[str, Any]]


class DeveloperResponse(BaseModel):
    id: int
    name: str
    role_type: str
    hourly_rate: int
    skills: List[str]
    seniority: str
    is_available: bool
    current_workload_hours: int
    workload_status: Optional[str] = None


class DeveloperCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    role_type: str = Field(..., min_length=2, max_length=50)
    hourly_rate: int = Field(..., ge=100, le=10000)
    skills: List[str] = Field(..., min_length=1)
    seniority: str = Field(..., pattern="^(junior|middle|senior|lead)$")
    is_available: bool = True

    @field_validator('skills')
    @classmethod
    def validate_skills(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Необходимо указать хотя бы один навык')
        return [skill.strip().lower() for skill in v if skill.strip()]


class TaskUpdateRequest(BaseModel):
    status: TaskStatusEnum = Field(..., description="New task status")
    actual_hours: Optional[int] = Field(None, ge=0, le=1000, description="Actual hours spent on task")
    comment: Optional[str] = Field(None, max_length=500, description="Optional comment about the update")

    @field_validator('actual_hours')
    @classmethod
    def validate_hours(cls, v):
        if v is not None and v < 0:
            raise ValueError('Количество часов не может быть отрицательным')
        return v


class ProjectQueueResponse(BaseModel):
    queue: List[Dict[str, Any]]
    total_projects: int
    generated_at: str


class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


# Dependency functions
async def get_project_system():
    """Dependency for getting project management system instance"""
    global project_system
    if project_system is None:
        raise HTTPException(
            status_code=503,
            detail="Project system not initialized. Please check database connection."
        )
    return project_system


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    global project_system
    try:
        logger.info("Initializing Project Management System...")

        # Initialize the system with database URL
        project_system = ProjectManagementSystem(DATABASE_URL)

        # Initialize database connection and tables
        await project_system.init_db()

        logger.info("✅ Project Management System initialized successfully!")
        logger.info("📊 Database tables created and populated with default developers")

    except Exception as e:
        logger.error(f"❌ Failed to initialize Project Management System: {e}")
        logger.error("🔧 Please check:")
        logger.error("   1. PostgreSQL is running")
        logger.error("   2. Database connection string is correct")
        logger.error("   3. Database exists and is accessible")
        # Keep project_system as None so dependency will fail properly


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup when shutting down the application"""
    global project_system
    if project_system:
        logger.info("Closing Project Management System...")
        await project_system.close()
        logger.info("✅ Project Management System closed successfully")


# API Routes
@app.post("/projects", response_model=ProjectResponse)
async def create_project(
        request: ProjectCreateRequest,
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """
    Create a new project from description

    The system automatically:
    - Classifies project type
    - Generates task list
    - Assigns developers
    - Plans time slots
    - Calculates costs
    """
    try:
        logger.info(f"Creating new project: {request.title or 'Untitled'}")

        result = await system.create_project_from_description(
            description=request.description,
            title=request.title
        )

        # If client info is provided, you can extend the system to handle it
        if any([request.client_name, request.client_email, request.client_phone,
                request.client_company, request.client_notes]):
            logger.info(f"Client info: {request.client_name}, {request.client_email}")
            # TODO: Implement update_project_client_info method

        logger.info(f"Project created successfully: {result['project']['id']}")
        return JSONResponse(content=result)

    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")


@app.get("/projects/queue", response_model=ProjectQueueResponse)
async def get_project_queue(
        status: Optional[ProjectStatusEnum] = Query(None, description="Filter by project status"),
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """
    Get project queue with time slot information

    Shows:
    - Project execution sequence
    - Current progress of each project
    - Planned start and end dates
    - Team workload
    """
    try:
        logger.info(f"Getting project queue, filter: {status}")

        queue = await system.get_project_queue()

        # Filter by status if specified
        if status:
            queue["queue"] = [p for p in queue["queue"] if p["status"] == status.value]
            queue["total_projects"] = len(queue["queue"])

        return JSONResponse(content=queue)

    except Exception as e:
        logger.error(f"Error getting project queue: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting project queue: {str(e)}")


@app.get("/projects/{project_id}")
async def get_project_details(
        project_id: str,
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """Get detailed project information"""
    try:
        logger.info(f"Getting project details for: {project_id}")

        project_details = await system.get_project_details(project_id)

        if "error" in project_details:
            raise HTTPException(status_code=404, detail=project_details["error"])

        return JSONResponse(content=project_details)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project details: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting project details: {str(e)}")


@app.get("/developers", response_model=List[DeveloperResponse])
async def get_developers(
        available_only: bool = Query(False, description="Show only available developers"),
        skills: Optional[List[str]] = Query(None, description="Filter by skills"),
        role_type: Optional[str] = Query(None, description="Filter by role type"),
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """
    Get list of developers with workload information

    Parameters:
    - available_only: show only available developers
    - skills: filter by skills (e.g., ?skills=python&skills=react)
    - role_type: filter by role type
    """
    try:
        logger.info(f"Getting developers, filters: available={available_only}, skills={skills}, role={role_type}")

        developers = await system.get_available_developers()

        # Filter by availability if requested
        if available_only:
            developers = [dev for dev in developers if dev.is_available]

        # Filter by role type if requested
        if role_type:
            developers = [dev for dev in developers if dev.role_type.lower() == role_type.lower()]

        # Filter by skills if requested
        if skills:
            developers = [
                dev for dev in developers
                if any(skill.lower() in [s.lower() for s in dev.skills] for skill in skills)
            ]

        # Convert to dict format for response
        developer_dicts = []
        for dev in developers:
            dev_dict = {
                "id": dev.id,
                "name": dev.name,
                "role_type": dev.role_type,
                "hourly_rate": dev.hourly_rate,
                "skills": dev.skills,
                "seniority": dev.seniority,
                "is_available": dev.is_available,
                "current_workload_hours": dev.current_workload_hours,
                "workload_status": "available" if dev.current_workload_hours < 40 else "busy"
            }
            developer_dicts.append(dev_dict)

        return JSONResponse(content=developer_dicts)

    except Exception as e:
        logger.error(f"Error getting developers: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting developers: {str(e)}")


@app.put("/tasks/{task_id}")
async def update_task(
        task_id: str,
        request: TaskUpdateRequest,
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """
    Update task status

    Automatically:
    - Logs changes
    - Recalculates developer workload
    - Updates project progress
    - Adjusts plans for subsequent tasks
    """
    try:
        logger.info(f"Updating task {task_id}: status={request.status}, hours={request.actual_hours}")

        # Проверяем, что передан хотя бы статус
        if not request.status:
            raise HTTPException(status_code=400, detail="Status is required for task update")

        result = await system.update_task_status(
            task_id=task_id,
            new_status=request.status.value,
            actual_hours=request.actual_hours
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


@app.get("/analytics/timeline")
async def get_timeline_analytics(
        project_id: Optional[str] = Query(None, description="Specific project ID for analysis"),
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """
    Timeline analytics for projects

    Shows:
    - Team workload by day
    - Critical points in plans
    - Optimization recommendations
    """
    try:
        logger.info(f"Getting timeline analytics for project: {project_id}")

        analytics = await system.get_timeline_analytics(project_id)

        return JSONResponse(content=analytics)

    except Exception as e:
        logger.error(f"Error getting timeline analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting timeline analytics: {str(e)}")


@app.get("/analytics/costs")
async def get_cost_analytics(
        project_id: Optional[str] = Query(None, description="Specific project ID for cost analysis"),
        developer_id: Optional[int] = Query(None, description="Specific developer ID for cost analysis"),
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """
    Project cost analytics

    Shows:
    - Breakdown by roles and tasks
    - Planned vs actual cost comparison
    - Team efficiency
    """
    try:
        logger.info(f"Getting cost analytics for project: {project_id}, developer: {developer_id}")

        analytics = await system.get_cost_analytics(project_id, developer_id)

        return JSONResponse(content=analytics)

    except Exception as e:
        logger.error(f"Error getting cost analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting cost analytics: {str(e)}")


@app.post("/developers")
async def add_developer(
        developer_data: DeveloperCreateRequest,
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """Add a new developer to the team"""
    try:
        logger.info(f"Adding new developer: {developer_data.name}")

        result = await system.add_developer(developer_data.dict())

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding developer: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding developer: {str(e)}")


@app.put("/developers/{developer_id}/availability")
async def update_developer_availability(
        developer_id: int,
        is_available: bool = Query(..., description="Developer availability status"),
        workload_hours: Optional[int] = Query(None, ge=0, le=80, description="Current workload hours"),
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """Update developer availability"""
    try:
        logger.info(f"Updating developer {developer_id} availability: {is_available}")

        result = await system.update_developer_availability(
            developer_id, is_available, workload_hours
        )

        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating developer availability: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating developer availability: {str(e)}")


# Дополнительные эндпоинты для работы с задачами
@app.get("/tasks/{task_id}")
async def get_task_details(
        task_id: str,
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """Get detailed information about a specific task"""
    try:
        logger.info(f"Getting task details for: {task_id}")

        # Поскольку у вас нет отдельного метода get_task_details,
        # используем базовый SQL запрос
        async with system.pool.acquire() as conn:
            task = await conn.fetchrow("""
                SELECT t.*, d.name as developer_name, d.role_type, d.hourly_rate,
                       p.title as project_title
                FROM tasks t
                LEFT JOIN developers d ON t.assigned_developer_id = d.id
                LEFT JOIN projects p ON t.project_id = p.id
                WHERE t.id = $1
            """, task_id)

            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

            task_data = {
                "id": task['id'],
                "title": task['title'],
                "description": task['description'],
                "category": task['category'],
                "complexity": task['complexity'],
                "status": task['status'],
                "estimated_hours": task['estimated_hours'],
                "actual_hours": task['actual_hours'],
                "start_date": task['start_date'].isoformat() if task['start_date'] else None,
                "end_date": task['end_date'].isoformat() if task['end_date'] else None,
                "created_at": task['created_at'].isoformat() if task['created_at'] else None,
                "project": {
                    "id": task['project_id'],
                    "title": task['project_title']
                },
                "assigned_developer": {
                    "id": task['assigned_developer_id'],
                    "name": task['developer_name'],
                    "role": task['role_type'],
                    "hourly_rate": task['hourly_rate']
                } if task['assigned_developer_id'] else None
            }

            return JSONResponse(content=task_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting task details: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting task details: {str(e)}")


@app.get("/projects/{project_id}/tasks")
async def get_project_tasks(
        project_id: str,
        status: Optional[TaskStatusEnum] = Query(None, description="Filter tasks by status"),
        developer_id: Optional[int] = Query(None, description="Filter tasks by developer"),
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """Get all tasks for a specific project with optional filters"""
    try:
        logger.info(f"Getting tasks for project {project_id}, filters: status={status}, developer={developer_id}")

        async with system.pool.acquire() as conn:
            base_query = """
                SELECT t.*, d.name as developer_name, d.role_type
                FROM tasks t
                LEFT JOIN developers d ON t.assigned_developer_id = d.id
                WHERE t.project_id = $1
            """
            params = [project_id]

            if status:
                base_query += " AND t.status = $2"
                params.append(status.value)

            if developer_id:
                if status:
                    base_query += " AND t.assigned_developer_id = $3"
                else:
                    base_query += " AND t.assigned_developer_id = $2"
                params.append(developer_id)

            base_query += " ORDER BY t.created_at"

            tasks = await conn.fetch(base_query, *params)

            tasks_data = [
                {
                    "id": task['id'],
                    "title": task['title'],
                    "description": task['description'],
                    "category": task['category'],
                    "complexity": task['complexity'],
                    "status": task['status'],
                    "estimated_hours": task['estimated_hours'],
                    "actual_hours": task['actual_hours'],
                    "start_date": task['start_date'].isoformat() if task['start_date'] else None,
                    "end_date": task['end_date'].isoformat() if task['end_date'] else None,
                    "assigned_developer": {
                        "id": task['assigned_developer_id'],
                        "name": task['developer_name'],
                        "role": task['role_type']
                    } if task['assigned_developer_id'] else None
                }
                for task in tasks
            ]

            return JSONResponse(content={
                "project_id": project_id,
                "tasks": tasks_data,
                "total_tasks": len(tasks_data),
                "filtered_by": {
                    "status": status.value if status else None,
                    "developer_id": developer_id
                }
            })

    except Exception as e:
        logger.error(f"Error getting project tasks: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting project tasks: {str(e)}")


@app.post("/projects/{project_id}/client-info")
async def update_project_client_info(
        project_id: str,
        client_info: Dict[str, Any],
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """Update client information for a project"""
    try:
        logger.info(f"Updating client info for project: {project_id}")

        async with system.pool.acquire() as conn:
            # Проверяем существование проекта
            project_exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM projects WHERE id = $1)", project_id
            )

            if not project_exists:
                raise HTTPException(status_code=404, detail="Project not found")

            # Обновляем клиентскую информацию
            update_fields = []
            params = [project_id]
            param_index = 2

            allowed_fields = ['client_name', 'client_email', 'client_phone', 'client_company', 'client_notes']

            for field in allowed_fields:
                if field in client_info:
                    update_fields.append(f"{field} = ${param_index}")
                    params.append(client_info[field])
                    param_index += 1

            if not update_fields:
                raise HTTPException(status_code=400, detail="No valid client information provided")

            query = f"UPDATE projects SET {', '.join(update_fields)} WHERE id = $1"
            await conn.execute(query, *params)

            # Получаем обновленную информацию
            updated_project = await conn.fetchrow("""
                SELECT client_name, client_email, client_phone, client_company, client_notes
                FROM projects WHERE id = $1
            """, project_id)

            return JSONResponse(content={
                "success": True,
                "project_id": project_id,
                "client_info": {
                    "name": updated_project['client_name'],
                    "email": updated_project['client_email'],
                    "phone": updated_project['client_phone'],
                    "company": updated_project['client_company'],
                    "notes": updated_project['client_notes']
                },
                "updated_at": datetime.now().isoformat()
            })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating client info: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating client info: {str(e)}")


@app.get("/developers/workload")
async def get_developer_workload(
        developer_id: Optional[int] = Query(None, description="Specific developer ID"),
        system: ProjectManagementSystem = Depends(get_project_system)
):
    """Get developer workload information"""
    try:
        logger.info(f"Getting workload for developer: {developer_id}")

        workload = await system.get_developer_workload(developer_id)

        return JSONResponse(content=workload)

    except Exception as e:
        logger.error(f"Error getting developer workload: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting developer workload: {str(e)}")


@app.get("/health")
async def health_check():
    """API health check"""
    global project_system

    system_status = "initialized" if project_system is not None else "not_initialized"

    # Additional health checks can be added here
    health_data = {
        "status": "healthy" if project_system is not None else "degraded",
        "system_status": system_status,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

    # Try to check database connectivity if system is initialized
    if project_system is not None:
        try:
            # You can add a simple DB ping here
            health_data["database"] = "connected"
        except Exception as e:
            health_data["database"] = f"error: {str(e)}"
            health_data["status"] = "degraded"

    return health_data


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    logger.error(f"ValueError: {exc}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": "An unexpected error occurred"}
    )


# Example usage data for documentation
example_requests = {
    "create_project": {
        "title": "Лендинг для стартапа",
        "description": "Современный лендинг без бекенда с красивым дизайном и адаптивной версткой для стартапа",
        "client_name": "ООО Инновации",
        "client_email": "info@startup.com",
        "client_phone": "+7 (999) 123-45-67",
        "client_company": "Стартап Инкубатор",
        "priority": 2
    },
    "create_crm": {
        "title": "CRM система для продаж",
        "description": "Полнофункциональная CRM система с управлением клиентами, воронкой продаж, аналитикой и интеграцией с внешними сервисами",
        "client_name": "Торговая компания Альфа",
        "client_email": "manager@alpha-trade.com",
        "priority": 3
    },
    "add_developer": {
        "name": "Алексей Петров",
        "role_type": "frontend",
        "hourly_rate": 2500,
        "skills": ["react", "typescript", "sass", "figma"],
        "seniority": "middle",
        "is_available": True
    },
    "update_task": {
        "status": "in_progress",
        "actual_hours": 8,
        "comment": "Начал работу над задачей"
    },
    "update_client_info": {
        "client_name": "Новое имя клиента",
        "client_email": "new@email.com",
        "client_phone": "+7 (999) 888-77-66",
        "client_company": "Новая компания",
        "client_notes": "Дополнительные заметки о клиенте"
    }
}

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting Project Management API...")
    print("📚 Swagger UI will be available at: http://localhost:8000/docs")
    print("📋 ReDoc will be available at: http://localhost:8000/redoc")
    print("🏥 Health check at: http://localhost:8000/health")
    print()
    print("⚠️  IMPORTANT: Make sure to configure DATABASE_URL in the code!")
    print("   Current setting:", DATABASE_URL)
    print()

    uvicorn.run(
        "main:app",  # replace with your filename
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )