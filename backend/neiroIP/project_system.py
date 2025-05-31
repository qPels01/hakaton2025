import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import asyncpg
import asyncio
from contextlib import asynccontextmanager


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class ProjectStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Developer:
    id: int
    name: str
    role_type: str
    hourly_rate: int
    skills: List[str]
    seniority: str
    is_available: bool = True
    current_workload_hours: int = 0


@dataclass
class Task:
    id: str
    title: str
    description: str
    category: str
    complexity: str
    estimated_hours: int
    required_skills: List[str]
    dependencies: List[str]
    status: TaskStatus = TaskStatus.PENDING
    assigned_developer_id: Optional[int] = None
    actual_hours: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


@dataclass
class Project:
    id: str
    title: str
    description: str
    status: ProjectStatus
    created_at: datetime
    estimated_start_date: datetime
    estimated_end_date: datetime
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    total_estimated_hours: int = 0
    total_estimated_cost: int = 0
    tasks: List[Task] = None


@dataclass
class TaskAssignment:
    task: Task
    developer: Developer
    estimated_hours: int
    estimated_cost: int
    scheduled_start: datetime
    scheduled_end: datetime


class ProjectManagementSystem:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None

        # База знаний по ролям (теперь будет в БД)
        self.default_roles = {
            'frontend_junior': {
                'name': 'Frontend Developer (Junior)',
                'hourly_rate': 1500,
                'skills': ['html', 'css', 'javascript', 'react', 'vue', 'верстка', 'адаптивный дизайн'],
                'seniority': 'junior'
            },
            'frontend_middle': {
                'name': 'Frontend Developer (Middle)',
                'hourly_rate': 2500,
                'skills': ['html', 'css', 'javascript', 'react', 'vue', 'typescript', 'webpack', 'оптимизация',
                           'тестирование'],
                'seniority': 'middle'
            },
            'backend_junior': {
                'name': 'Backend Developer (Junior)',
                'hourly_rate': 1800,
                'skills': ['python', 'django', 'flask', 'api', 'база данных', 'sql'],
                'seniority': 'junior'
            },
            'backend_middle': {
                'name': 'Backend Developer (Middle)',
                'hourly_rate': 3000,
                'skills': ['python', 'django', 'flask', 'fastapi', 'postgresql', 'redis', 'celery', 'docker', 'api',
                           'микросервисы'],
                'seniority': 'middle'
            },
            'backend_senior': {
                'name': 'Backend Developer (Senior)',
                'hourly_rate': 4500,
                'skills': ['архитектура', 'микросервисы', 'highload', 'оптимизация', 'безопасность', 'devops',
                           'код-ревью'],
                'seniority': 'senior'
            },
            'ui_ux': {
                'name': 'UI/UX Designer',
                'hourly_rate': 2200,
                'skills': ['дизайн', 'интерфейс', 'прототипирование', 'пользовательский опыт', 'figma', 'адобе'],
                'seniority': 'middle'
            },
            'devops': {
                'name': 'DevOps Engineer',
                'hourly_rate': 3500,
                'skills': ['docker', 'kubernetes', 'ci/cd', 'aws', 'nginx', 'мониторинг', 'безопасность'],
                'seniority': 'middle'
            },
            'qa_tester': {
                'name': 'QA Tester',
                'hourly_rate': 2000,
                'skills': ['тестирование', 'автотесты', 'selenium', 'postman', 'баг-репорты'],
                'seniority': 'middle'
            }
        }

        # Шаблоны задач
        self.task_templates = {
            'сайт одностраничный': [
                {'title': 'Создание дизайн-макета', 'category': 'design', 'hours': 16, 'skills': ['дизайн', 'figma']},
                {'title': 'Верстка главной страницы', 'category': 'frontend', 'hours': 24,
                 'skills': ['html', 'css', 'javascript']},
                {'title': 'Адаптивная верстка', 'category': 'frontend', 'hours': 12,
                 'skills': ['css', 'адаптивный дизайн']},
                {'title': 'Интеграция с бэкендом', 'category': 'frontend', 'hours': 8, 'skills': ['javascript', 'api']},
                {'title': 'Тестирование и отладка', 'category': 'qa', 'hours': 8, 'skills': ['тестирование']}
            ],
            'crm система': [
                {'title': 'Проектирование архитектуры', 'category': 'architecture', 'hours': 16,
                 'skills': ['архитектура']},
                {'title': 'Настройка базы данных', 'category': 'backend', 'hours': 12,
                 'skills': ['postgresql', 'база данных']},
                {'title': 'API для управления пользователями', 'category': 'backend', 'hours': 20,
                 'skills': ['api', 'python']},
                {'title': 'Система аутентификации', 'category': 'backend', 'hours': 14,
                 'skills': ['безопасность', 'api']},
                {'title': 'Админ-панель', 'category': 'frontend', 'hours': 32, 'skills': ['react', 'javascript']},
                {'title': 'Пользовательский интерфейс', 'category': 'frontend', 'hours': 40,
                 'skills': ['react', 'css']},
                {'title': 'Интеграция и тестирование', 'category': 'qa', 'hours': 16, 'skills': ['тестирование']}
            ],
            'лендинг без бекенда': [
                {'title': 'Создание дизайн-макета', 'category': 'design', 'hours': 12, 'skills': ['дизайн', 'figma']},
                {'title': 'Верстка страницы', 'category': 'frontend', 'hours': 20,
                 'skills': ['html', 'css', 'javascript']},
                {'title': 'Адаптивная верстка', 'category': 'frontend', 'hours': 10,
                 'skills': ['css', 'адаптивный дизайн']},
                {'title': 'Тестирование', 'category': 'qa', 'hours': 6, 'skills': ['тестирование']}
            ]
        }

    async def init_db(self):
        """Инициализация подключения к базе данных"""
        self.pool = await asyncpg.create_pool(self.db_url)
        await self.create_tables()
        await self.populate_default_developers()

    async def create_tables(self):
        """Создание таблиц в базе данных"""
        async with self.pool.acquire() as conn:
            # Таблица разработчиков
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS developers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    role_type VARCHAR(100) NOT NULL,
                    hourly_rate INTEGER NOT NULL,
                    skills TEXT[] NOT NULL,
                    seniority VARCHAR(50) NOT NULL,
                    is_available BOOLEAN DEFAULT TRUE,
                    current_workload_hours INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Таблица проектов
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id VARCHAR(100) PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    estimated_start_date TIMESTAMP,
                    estimated_end_date TIMESTAMP,
                    actual_start_date TIMESTAMP,
                    actual_end_date TIMESTAMP,
                    total_estimated_hours INTEGER DEFAULT 0,
                    total_estimated_cost INTEGER DEFAULT 0
                )
            """)

            # Таблица задач
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id VARCHAR(100) PRIMARY KEY,
                    project_id VARCHAR(100) REFERENCES projects(id),
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    category VARCHAR(100),
                    complexity VARCHAR(50),
                    estimated_hours INTEGER,
                    required_skills TEXT[],
                    dependencies TEXT[],
                    status VARCHAR(50) DEFAULT 'pending',
                    assigned_developer_id INTEGER REFERENCES developers(id),
                    actual_hours INTEGER,
                    start_date TIMESTAMP,
                    end_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            print("Таблицы созданы успешно!")

    async def populate_default_developers(self):
        """Заполнение базы данных стандартными разработчиками"""
        async with self.pool.acquire() as conn:
            # Проверяем, есть ли уже разработчики
            count = await conn.fetchval("SELECT COUNT(*) FROM developers")

            if count == 0:
                for role_key, role_data in self.default_roles.items():
                    await conn.execute("""
                        INSERT INTO developers (name, role_type, hourly_rate, skills, seniority)
                        VALUES ($1, $2, $3, $4, $5)
                    """, role_data['name'], role_key, role_data['hourly_rate'],
                                       role_data['skills'], role_data['seniority'])

                print("Стандартные разработчики добавлены в базу данных!")

    async def get_available_developers(self) -> List[Developer]:
        """Получение списка доступных разработчиков"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT * FROM developers WHERE is_available = TRUE
                ORDER BY seniority, hourly_rate
            """)

            return [
                Developer(
                    id=row['id'],
                    name=row['name'],
                    role_type=row['role_type'],
                    hourly_rate=row['hourly_rate'],
                    skills=row['skills'],
                    seniority=row['seniority'],
                    is_available=row['is_available'],
                    current_workload_hours=row['current_workload_hours']
                )
                for row in rows
            ]

    async def find_next_available_slot(self, developer_id: int) -> datetime:
        """Находит следующий доступный слот для разработчика"""
        async with self.pool.acquire() as conn:
            # Получаем последнюю запланированную дату окончания работ
            last_end_date = await conn.fetchval("""
                SELECT MAX(end_date) FROM tasks 
                WHERE assigned_developer_id = $1 AND status IN ('pending', 'in_progress')
            """, developer_id)

            if last_end_date:
                return last_end_date
            else:
                return datetime.now()

    def classify_project_type(self, description: str) -> str:
        """Классификация типа проекта"""
        desc_lower = description.lower()

        if 'лендинг без бекенда' in desc_lower:
            return 'лендинг без бекенда'
        elif any(word in desc_lower for word in ['сайт', 'одностраничник', 'лендинг']):
            return 'сайт одностраничный'
        elif any(word in desc_lower for word in ['crm', 'система управления']):
            return 'crm система'
        else:
            return 'сайт одностраничный'  # по умолчанию

    def generate_tasks_from_template(self, project_type: str, project_id: str) -> List[Task]:
        """Генерация задач из шаблона"""
        template = self.task_templates.get(project_type, self.task_templates['сайт одностраничный'])
        tasks = []

        for i, task_config in enumerate(template):
            task = Task(
                id=f"{project_id}_task_{i + 1}",
                title=task_config['title'],
                description=f"Реализация: {task_config['title']}",
                category=task_config['category'],
                complexity='medium',
                estimated_hours=task_config['hours'],
                required_skills=task_config['skills'],
                dependencies=[]
            )
            tasks.append(task)

        return tasks

    def find_best_developer(self, task: Task, available_developers: List[Developer]) -> Developer:
        """Поиск наиболее подходящего разработчика для задачи"""
        scores = {}

        for dev in available_developers:
            score = 0

            # Совпадение навыков
            matching_skills = len(set(task.required_skills) & set(dev.skills))
            score += matching_skills * 10

            # Соответствие категории
            if task.category == 'frontend' and 'frontend' in dev.role_type:
                score += 20
            elif task.category == 'backend' and 'backend' in dev.role_type:
                score += 20
            elif task.category == 'design' and 'ui_ux' in dev.role_type:
                score += 20
            elif task.category == 'qa' and 'qa' in dev.role_type:
                score += 20

            # Штраф за неподходящий уровень
            if task.complexity == 'high' and dev.seniority == 'junior':
                score -= 10

            scores[dev.id] = score

        if not scores:
            return available_developers[0] if available_developers else None

        best_dev_id = max(scores, key=scores.get)
        return next(dev for dev in available_developers if dev.id == best_dev_id)

    async def create_project_from_description(self, description: str, title: str = None) -> Dict:
        """Создание проекта из описания с планированием времени"""
        project_id = f"proj_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        project_type = self.classify_project_type(description)

        if not title:
            title = f"Проект: {project_type}"

        # Генерируем задачи
        tasks = self.generate_tasks_from_template(project_type, project_id)

        # Получаем доступных разработчиков
        available_developers = await self.get_available_developers()

        # Планируем задачи и назначаем разработчиков
        assignments = []
        current_start_time = datetime.now()

        for task in tasks:
            best_dev = self.find_best_developer(task, available_developers)

            if best_dev:
                # Находим следующий доступный слот для разработчика
                start_time = await self.find_next_available_slot(best_dev.id)
                if start_time < current_start_time:
                    start_time = current_start_time

                # Корректируем время в зависимости от уровня разработчика
                adjusted_hours = self.adjust_hours_for_seniority(
                    task.estimated_hours, best_dev.seniority, task.complexity
                )

                # Рассчитываем время окончания (8 часов рабочий день)
                working_days = adjusted_hours / 8
                end_time = start_time + timedelta(days=working_days)

                cost = adjusted_hours * best_dev.hourly_rate

                assignment = TaskAssignment(
                    task=task,
                    developer=best_dev,
                    estimated_hours=adjusted_hours,
                    estimated_cost=cost,
                    scheduled_start=start_time,
                    scheduled_end=end_time
                )

                assignments.append(assignment)

                # Обновляем время начала для следующих задач
                current_start_time = max(current_start_time, end_time)

        # Сохраняем проект в базу данных
        await self.save_project_to_db(project_id, title, description, assignments)

        # Формируем JSON ответ
        return self.generate_json_response(project_id, title, description, assignments)

    def adjust_hours_for_seniority(self, base_hours: int, seniority: str, complexity: str) -> int:
        """Корректировка времени в зависимости от уровня разработчика"""
        multiplier = 1.0

        if seniority == 'junior':
            multiplier = 1.3 if complexity in ['medium', 'high'] else 1.1
        elif seniority == 'senior':
            multiplier = 0.8 if complexity == 'low' else 0.9

        return int(base_hours * multiplier)

    async def save_project_to_db(self, project_id: str, title: str, description: str,
                                 assignments: List[TaskAssignment]):
        """Сохранение проекта и задач в базу данных"""
        async with self.pool.acquire() as conn:
            # Вычисляем общие показатели
            total_hours = sum(a.estimated_hours for a in assignments)
            total_cost = sum(a.estimated_cost for a in assignments)

            project_start = min(a.scheduled_start for a in assignments) if assignments else datetime.now()
            project_end = max(a.scheduled_end for a in assignments) if assignments else datetime.now()

            # Сохраняем проект
            await conn.execute("""
                INSERT INTO projects (id, title, description, status, estimated_start_date, 
                                    estimated_end_date, total_estimated_hours, total_estimated_cost)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """, project_id, title, description, ProjectStatus.PLANNED.value,
                               project_start, project_end, total_hours, total_cost)

            # Сохраняем задачи
            for assignment in assignments:
                task = assignment.task
                await conn.execute("""
                    INSERT INTO tasks (id, project_id, title, description, category, complexity,
                                     estimated_hours, required_skills, dependencies, assigned_developer_id,
                                     start_date, end_date)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                """, task.id, project_id, task.title, task.description, task.category,
                                   task.complexity, assignment.estimated_hours, task.required_skills,
                                   task.dependencies, assignment.developer.id,
                                   assignment.scheduled_start, assignment.scheduled_end)

    def generate_json_response(self, project_id: str, title: str, description: str,
                               assignments: List[TaskAssignment]) -> Dict:
        """Генерация JSON ответа"""
        total_hours = sum(a.estimated_hours for a in assignments)
        total_cost = sum(a.estimated_cost for a in assignments)

        project_start = min(a.scheduled_start for a in assignments) if assignments else datetime.now()
        project_end = max(a.scheduled_end for a in assignments) if assignments else datetime.now()

        # Группировка по разработчикам
        developers_summary = {}
        for assignment in assignments:
            dev_name = assignment.developer.name
            if dev_name not in developers_summary:
                developers_summary[dev_name] = {
                    "developer_id": assignment.developer.id,
                    "role": assignment.developer.role_type,
                    "hourly_rate": assignment.developer.hourly_rate,
                    "total_hours": 0,
                    "total_cost": 0,
                    "tasks": []
                }

            developers_summary[dev_name]["total_hours"] += assignment.estimated_hours
            developers_summary[dev_name]["total_cost"] += assignment.estimated_cost
            developers_summary[dev_name]["tasks"].append({
                "task_id": assignment.task.id,
                "title": assignment.task.title,
                "hours": assignment.estimated_hours,
                "start_date": assignment.scheduled_start.isoformat(),
                "end_date": assignment.scheduled_end.isoformat()
            })

        return {
            "project": {
                "id": project_id,
                "title": title,
                "description": description,
                "status": "planned",
                "created_at": datetime.now().isoformat()
            },
            "timeline": {
                "estimated_start": project_start.isoformat(),
                "estimated_end": project_end.isoformat(),
                "duration_days": (project_end - project_start).days,
                "total_hours": total_hours,
                "total_cost": total_cost
            },
            "team_assignment": developers_summary,
            "detailed_tasks": [
                {
                    "task_id": a.task.id,
                    "title": a.task.title,
                    "description": a.task.description,
                    "category": a.task.category,
                    "complexity": a.task.complexity,
                    "assigned_developer": a.developer.name,
                    "developer_id": a.developer.id,
                    "estimated_hours": a.estimated_hours,
                    "estimated_cost": a.estimated_cost,
                    "scheduled_start": a.scheduled_start.isoformat(),
                    "scheduled_end": a.scheduled_end.isoformat(),
                    "status": "pending"
                }
                for a in assignments
            ]
        }

    async def get_project_queue(self) -> Dict:
        """Получение очереди проектов с временными слотами"""
        async with self.pool.acquire() as conn:
            projects = await conn.fetch("""
                SELECT p.*, 
                       COUNT(t.id) as total_tasks,
                       COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
                GROUP BY p.id
                ORDER BY p.estimated_start_date
            """)

            queue = []
            for project in projects:
                progress = 0
                if project['total_tasks'] > 0:
                    progress = (project['completed_tasks'] / project['total_tasks']) * 100

                queue.append({
                    "project_id": project['id'],
                    "title": project['title'],
                    "status": project['status'],
                    "estimated_start": project['estimated_start_date'].isoformat() if project[
                        'estimated_start_date'] else None,
                    "estimated_end": project['estimated_end_date'].isoformat() if project[
                        'estimated_end_date'] else None,
                    "total_hours": project['total_estimated_hours'],
                    "total_cost": project['total_estimated_cost'],
                    "progress_percent": round(progress, 1),
                    "total_tasks": project['total_tasks'],
                    "completed_tasks": project['completed_tasks']
                })

            return {
                "queue": queue,
                "total_projects": len(queue),
                "generated_at": datetime.now().isoformat()
            }

    async def close(self):
        """Закрытие соединения с базой данных"""
        if self.pool:
            await self.pool.close()

    async def update_project_client_info(self, project_id: str, client_info: Dict) -> Dict:
        """Обновление информации о клиенте для проекта"""
        async with self.pool.acquire() as conn:
            # Сначала проверяем, существует ли проект
            project_exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM projects WHERE id = $1)", project_id
            )

            if not project_exists:
                return {"error": "Проект не найден", "project_id": project_id}

            # Добавляем поля для клиентской информации в существующую таблицу
            try:
                await conn.execute("""
                    ALTER TABLE projects 
                    ADD COLUMN IF NOT EXISTS client_name VARCHAR(255),
                    ADD COLUMN IF NOT EXISTS client_email VARCHAR(255),
                    ADD COLUMN IF NOT EXISTS client_phone VARCHAR(50),
                    ADD COLUMN IF NOT EXISTS client_company VARCHAR(255),
                    ADD COLUMN IF NOT EXISTS client_notes TEXT
                """)
            except Exception:
                pass  # Колонки уже существуют

            # Обновляем информацию о клиенте
            await conn.execute("""
                UPDATE projects 
                SET client_name = $2, client_email = $3, client_phone = $4, 
                    client_company = $5, client_notes = $6
                WHERE id = $1
            """, project_id,
                               client_info.get('name'),
                               client_info.get('email'),
                               client_info.get('phone'),
                               client_info.get('company'),
                               client_info.get('notes')
                               )

            return {
                "success": True,
                "project_id": project_id,
                "client_info": client_info,
                "updated_at": datetime.now().isoformat()
            }

    async def get_project_details(self, project_id: str) -> Dict:
        """Получение детальной информации о проекте"""
        async with self.pool.acquire() as conn:
            # Получаем основную информацию о проекте
            project = await conn.fetchrow("""
                SELECT * FROM projects WHERE id = $1
            """, project_id)

            if not project:
                return {"error": "Проект не найден", "project_id": project_id}

            # Получаем задачи проекта с назначенными разработчиками
            tasks = await conn.fetch("""
                SELECT t.*, d.name as developer_name, d.role_type, d.hourly_rate
                FROM tasks t
                LEFT JOIN developers d ON t.assigned_developer_id = d.id
                WHERE t.project_id = $1
                ORDER BY t.created_at
            """, project_id)

            # Подсчитываем статистику
            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if task['status'] == 'completed')
            in_progress_tasks = sum(1 for task in tasks if task['status'] == 'in_progress')
            pending_tasks = sum(1 for task in tasks if task['status'] == 'pending')

            actual_hours = sum(task['actual_hours'] or 0 for task in tasks)
            estimated_hours = sum(task['estimated_hours'] or 0 for task in tasks)

            progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

            # Формируем детализированный ответ
            return {
                "project": {
                    "id": project['id'],
                    "title": project['title'],
                    "description": project['description'],
                    "status": project['status'],
                    "created_at": project['created_at'].isoformat() if project['created_at'] else None,
                    "estimated_start_date": project['estimated_start_date'].isoformat() if project[
                        'estimated_start_date'] else None,
                    "estimated_end_date": project['estimated_end_date'].isoformat() if project[
                        'estimated_end_date'] else None,
                    "actual_start_date": project['actual_start_date'].isoformat() if project[
                        'actual_start_date'] else None,
                    "actual_end_date": project['actual_end_date'].isoformat() if project['actual_end_date'] else None,
                    "client_info": {
                        "name": project.get('client_name'),
                        "email": project.get('client_email'),
                        "phone": project.get('client_phone'),
                        "company": project.get('client_company'),
                        "notes": project.get('client_notes')
                    }
                },
                "statistics": {
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "in_progress_tasks": in_progress_tasks,
                    "pending_tasks": pending_tasks,
                    "progress_percent": round(progress, 1),
                    "estimated_hours": estimated_hours,
                    "actual_hours": actual_hours,
                    "estimated_cost": project['total_estimated_cost'],
                    "efficiency": round((estimated_hours / actual_hours * 100), 1) if actual_hours > 0 else 0
                },
                "tasks": [
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
                            "role": task['role_type'],
                            "hourly_rate": task['hourly_rate']
                        } if task['assigned_developer_id'] else None
                    }
                    for task in tasks
                ]
            }

    async def update_task_status(self, task_id: str, new_status: str, actual_hours: int = None) -> Dict:
        """Обновление статуса задачи"""
        valid_statuses = ['pending', 'in_progress', 'completed', 'blocked', 'cancelled']

        if new_status not in valid_statuses:
            return {
                "error": f"Недопустимый статус. Допустимые значения: {', '.join(valid_statuses)}",
                "task_id": task_id
            }

        async with self.pool.acquire() as conn:
            # Проверяем существование задачи
            task_exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM tasks WHERE id = $1)", task_id
            )

            if not task_exists:
                return {"error": "Задача не найдена", "task_id": task_id}

            # Обновляем статус и актуальные часы
            update_fields = ["status = $2"]
            params = [task_id, new_status]

            if actual_hours is not None:
                update_fields.append("actual_hours = $3")
                params.append(actual_hours)

            # Обновляем даты в зависимости от статуса
            if new_status == 'in_progress':
                update_fields.append("start_date = CURRENT_TIMESTAMP")
            elif new_status == 'completed':
                update_fields.append("end_date = CURRENT_TIMESTAMP")

            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = $1"
            await conn.execute(query, *params)

            # Получаем обновленную информацию о задаче
            updated_task = await conn.fetchrow("""
                SELECT t.*, d.name as developer_name 
                FROM tasks t
                LEFT JOIN developers d ON t.assigned_developer_id = d.id
                WHERE t.id = $1
            """, task_id)

            return {
                "success": True,
                "task": {
                    "id": updated_task['id'],
                    "title": updated_task['title'],
                    "status": updated_task['status'],
                    "actual_hours": updated_task['actual_hours'],
                    "assigned_developer": updated_task['developer_name'],
                    "updated_at": datetime.now().isoformat()
                }
            }

    async def get_timeline_analytics(self, project_id: str = None) -> Dict:
        """Получение аналитики по временным показателям"""
        async with self.pool.acquire() as conn:
            base_query = """
                SELECT 
                    p.id as project_id,
                    p.title,
                    p.status,
                    p.estimated_start_date,
                    p.estimated_end_date,
                    p.actual_start_date,
                    p.actual_end_date,
                    COUNT(t.id) as total_tasks,
                    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
                    SUM(t.estimated_hours) as total_estimated_hours,
                    SUM(t.actual_hours) as total_actual_hours
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
            """

            if project_id:
                base_query += " WHERE p.id = $1"
                projects = await conn.fetch(base_query + " GROUP BY p.id", project_id)
            else:
                projects = await conn.fetch(base_query + " GROUP BY p.id ORDER BY p.created_at DESC")

            analytics = []

            for project in projects:
                estimated_duration = None
                actual_duration = None
                delay_days = 0

                if project['estimated_start_date'] and project['estimated_end_date']:
                    estimated_duration = (project['estimated_end_date'] - project['estimated_start_date']).days

                if project['actual_start_date'] and project['actual_end_date']:
                    actual_duration = (project['actual_end_date'] - project['actual_start_date']).days

                if project['estimated_end_date'] and project['actual_end_date']:
                    delay_days = (project['actual_end_date'] - project['estimated_end_date']).days

                progress = 0
                if project['total_tasks'] > 0:
                    progress = (project['completed_tasks'] / project['total_tasks']) * 100

                efficiency = 0
                if project['total_actual_hours'] and project['total_estimated_hours']:
                    efficiency = (project['total_estimated_hours'] / project['total_actual_hours']) * 100

                analytics.append({
                    "project_id": project['project_id'],
                    "title": project['title'],
                    "status": project['status'],
                    "progress_percent": round(progress, 1),
                    "estimated_duration_days": estimated_duration,
                    "actual_duration_days": actual_duration,
                    "delay_days": delay_days,
                    "estimated_hours": project['total_estimated_hours'] or 0,
                    "actual_hours": project['total_actual_hours'] or 0,
                    "efficiency_percent": round(efficiency, 1),
                    "on_schedule": delay_days <= 0 if delay_days is not None else None
                })

            return {
                "timeline_analytics": analytics,
                "summary": {
                    "total_projects": len(analytics),
                    "on_schedule": sum(1 for a in analytics if a['on_schedule'] is True),
                    "delayed": sum(1 for a in analytics if a['on_schedule'] is False),
                    "average_efficiency": round(
                        sum(a['efficiency_percent'] for a in analytics if a['efficiency_percent'] > 0) /
                        len([a for a in analytics if a['efficiency_percent'] > 0]), 1
                    ) if analytics else 0
                },
                "generated_at": datetime.now().isoformat()
            }

    async def get_cost_analytics(self, project_id: str = None, developer_id: int = None) -> Dict:
        """Получение аналитики по стоимости"""
        async with self.pool.acquire() as conn:
            analytics = {}

            # Аналитика по проектам
            if project_id:
                project_query = """
                    SELECT 
                        p.id, p.title, p.total_estimated_cost,
                        SUM(t.actual_hours * d.hourly_rate) as actual_cost,
                        SUM(t.estimated_hours) as estimated_hours,
                        SUM(t.actual_hours) as actual_hours
                    FROM projects p
                    LEFT JOIN tasks t ON p.id = t.project_id
                    LEFT JOIN developers d ON t.assigned_developer_id = d.id
                    WHERE p.id = $1
                    GROUP BY p.id
                """
                project_data = await conn.fetchrow(project_query, project_id)
            else:
                project_query = """
                    SELECT 
                        p.id, p.title, p.total_estimated_cost,
                        SUM(t.actual_hours * d.hourly_rate) as actual_cost,
                        SUM(t.estimated_hours) as estimated_hours,
                        SUM(t.actual_hours) as actual_hours
                    FROM projects p
                    LEFT JOIN tasks t ON p.id = t.project_id
                    LEFT JOIN developers d ON t.assigned_developer_id = d.id
                    GROUP BY p.id
                    ORDER BY p.created_at DESC
                """
                project_data = await conn.fetch(project_query)

            # Аналитика по разработчикам
            dev_query = """
                SELECT 
                    d.id, d.name, d.role_type, d.hourly_rate,
                    COUNT(t.id) as total_tasks,
                    SUM(t.estimated_hours) as estimated_hours,
                    SUM(t.actual_hours) as actual_hours,
                    SUM(t.actual_hours * d.hourly_rate) as total_earned
                FROM developers d
                LEFT JOIN tasks t ON d.id = t.assigned_developer_id
            """

            if developer_id:
                dev_query += " WHERE d.id = $1"
                dev_data = await conn.fetchrow(dev_query + " GROUP BY d.id", developer_id)
            else:
                dev_data = await conn.fetch(dev_query + " GROUP BY d.id ORDER BY total_earned DESC")

            # Формируем результат
            if project_id and project_data:
                cost_variance = (project_data['actual_cost'] or 0) - (project_data['total_estimated_cost'] or 0)
                analytics['project'] = {
                    "id": project_data['id'],
                    "title": project_data['title'],
                    "estimated_cost": project_data['total_estimated_cost'] or 0,
                    "actual_cost": project_data['actual_cost'] or 0,
                    "cost_variance": cost_variance,
                    "cost_variance_percent": round((cost_variance / project_data['total_estimated_cost'] * 100), 1) if
                    project_data['total_estimated_cost'] else 0
                }
            elif not project_id:
                analytics['projects'] = []
                for proj in project_data:
                    cost_variance = (proj['actual_cost'] or 0) - (proj['total_estimated_cost'] or 0)
                    analytics['projects'].append({
                        "id": proj['id'],
                        "title": proj['title'],
                        "estimated_cost": proj['total_estimated_cost'] or 0,
                        "actual_cost": proj['actual_cost'] or 0,
                        "cost_variance": cost_variance,
                        "cost_variance_percent": round((cost_variance / proj['total_estimated_cost'] * 100), 1) if proj[
                            'total_estimated_cost'] else 0
                    })

            if developer_id and dev_data:
                analytics['developer'] = {
                    "id": dev_data['id'],
                    "name": dev_data['name'],
                    "role": dev_data['role_type'],
                    "hourly_rate": dev_data['hourly_rate'],
                    "total_tasks": dev_data['total_tasks'] or 0,
                    "total_hours": dev_data['actual_hours'] or 0,
                    "total_earned": dev_data['total_earned'] or 0,
                    "efficiency": round((dev_data['estimated_hours'] / dev_data['actual_hours'] * 100), 1) if dev_data[
                        'actual_hours'] else 0
                }
            elif not developer_id:
                analytics['developers'] = []
                for dev in dev_data:
                    analytics['developers'].append({
                        "id": dev['id'],
                        "name": dev['name'],
                        "role": dev['role_type'],
                        "hourly_rate": dev['hourly_rate'],
                        "total_tasks": dev['total_tasks'] or 0,
                        "total_hours": dev['actual_hours'] or 0,
                        "total_earned": dev['total_earned'] or 0,
                        "efficiency": round((dev['estimated_hours'] / dev['actual_hours'] * 100), 1) if dev[
                            'actual_hours'] else 0
                    })

            analytics['generated_at'] = datetime.now().isoformat()
            return analytics

    async def add_developer(self, developer_data: Dict) -> Dict:
        """Добавление нового разработчика"""
        required_fields = ['name', 'role_type', 'hourly_rate', 'skills', 'seniority']

        for field in required_fields:
            if field not in developer_data:
                return {"error": f"Отсутствует обязательное поле: {field}"}

        async with self.pool.acquire() as conn:
            try:
                # Добавляем разработчика
                developer_id = await conn.fetchval("""
                    INSERT INTO developers (name, role_type, hourly_rate, skills, seniority, is_available)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                """,
                                                   developer_data['name'],
                                                   developer_data['role_type'],
                                                   developer_data['hourly_rate'],
                                                   developer_data['skills'],
                                                   developer_data['seniority'],
                                                   developer_data.get('is_available', True)
                                                   )

                return {
                    "success": True,
                    "developer": {
                        "id": developer_id,
                        "name": developer_data['name'],
                        "role_type": developer_data['role_type'],
                        "hourly_rate": developer_data['hourly_rate'],
                        "skills": developer_data['skills'],
                        "seniority": developer_data['seniority'],
                        "is_available": developer_data.get('is_available', True),
                        "created_at": datetime.now().isoformat()
                    }
                }
            except Exception as e:
                return {"error": f"Ошибка при добавлении разработчика: {str(e)}"}

    async def update_developer_availability(self, developer_id: int, is_available: bool,
                                            workload_hours: int = None) -> Dict:
        """Обновление доступности разработчика"""
        async with self.pool.acquire() as conn:
            # Проверяем существование разработчика
            developer_exists = await conn.fetchval(
                "SELECT EXISTS(SELECT 1 FROM developers WHERE id = $1)", developer_id
            )

            if not developer_exists:
                return {"error": "Разработчик не найден", "developer_id": developer_id}

            # Обновляем доступность
            update_fields = ["is_available = $2"]
            params = [developer_id, is_available]

            if workload_hours is not None:
                update_fields.append("current_workload_hours = $3")
                params.append(workload_hours)

            query = f"UPDATE developers SET {', '.join(update_fields)} WHERE id = $1"
            await conn.execute(query, *params)

            # Получаем обновленную информацию
            updated_developer = await conn.fetchrow("""
                SELECT * FROM developers WHERE id = $1
            """, developer_id)

            return {
                "success": True,
                "developer": {
                    "id": updated_developer['id'],
                    "name": updated_developer['name'],
                    "role_type": updated_developer['role_type'],
                    "is_available": updated_developer['is_available'],
                    "current_workload_hours": updated_developer['current_workload_hours'],
                    "updated_at": datetime.now().isoformat()
                }
            }

    async def get_developer_workload(self, developer_id: int = None) -> Dict:
        """Получение информации о загруженности разработчиков"""
        async with self.pool.acquire() as conn:
            base_query = """
                SELECT 
                    d.*,
                    COUNT(CASE WHEN t.status IN ('pending', 'in_progress') THEN 1 END) as active_tasks,
                    SUM(CASE WHEN t.status IN ('pending', 'in_progress') THEN t.estimated_hours END) as pending_hours,
                    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
                    SUM(CASE WHEN t.status = 'completed' THEN t.actual_hours END) as completed_hours
                FROM developers d
                LEFT JOIN tasks t ON d.id = t.assigned_developer_id
            """

            if developer_id:
                base_query += " WHERE d.id = $1"
                developers = await conn.fetch(base_query + " GROUP BY d.id", developer_id)
            else:
                developers = await conn.fetch(base_query + " GROUP BY d.id ORDER BY d.name")

            workload_data = []

            for dev in developers:
                # Вычисляем процент загруженности (предполагаем 40 часов в неделю = 100%)
                workload_percent = ((dev['pending_hours'] or 0) / 40) * 100 if dev['pending_hours'] else 0

                workload_data.append({
                    "developer_id": dev['id'],
                    "name": dev['name'],
                    "role_type": dev['role_type'],
                    "is_available": dev['is_available'],
                    "active_tasks": dev['active_tasks'] or 0,
                    "pending_hours": dev['pending_hours'] or 0,
                    "completed_tasks": dev['completed_tasks'] or 0,
                    "completed_hours": dev['completed_hours'] or 0,
                    "workload_percent": round(min(workload_percent, 100), 1),
                    "status": "overloaded" if workload_percent > 100 else "busy" if workload_percent > 80 else "available"
                })

            return {
                "developers_workload": workload_data,
                "summary": {
                    "total_developers": len(workload_data),
                    "available": sum(1 for d in workload_data if d['status'] == 'available'),
                    "busy": sum(1 for d in workload_data if d['status'] == 'busy'),
                    "overloaded": sum(1 for d in workload_data if d['status'] == 'overloaded')
                },
                "generated_at": datetime.now().isoformat()
            }


# Пример использования
async def main():
    # Замените на ваши настройки подключения к PostgreSQL
    DB_URL = "postgresql://postgres:user@localhost:5432/project_management"

    system = ProjectManagementSystem(DB_URL)

    try:
        await system.init_db()

        # Создаем тестовый проект
        result = await system.create_project_from_description(
            "Лендинг без бекенда",
            "Лендинг для стартапа"
        )

        print("=== РЕЗУЛЬТАТ В JSON ФОРМАТЕ ===")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # Получаем очередь проектов
        queue = await system.get_project_queue()
        print("\n=== ОЧЕРЕДЬ ПРОЕКТОВ ===")
        print(json.dumps(queue, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        await system.close()


if __name__ == "__main__":
    asyncio.run(main())