-- Создание базы данных для системы управления проектами
-- PostgreSQL Schema

-- Удаление существующих таблиц (если нужно пересоздать)
DROP TABLE IF EXISTS task_dependencies CASCADE;
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS developers CASCADE;

-- Таблица разработчиков
CREATE TABLE developers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role_type VARCHAR(100) NOT NULL,
    hourly_rate INTEGER NOT NULL CHECK (hourly_rate > 0),
    skills TEXT[] NOT NULL,
    seniority VARCHAR(50) NOT NULL CHECK (seniority IN ('junior', 'middle', 'senior')),
    is_available BOOLEAN DEFAULT TRUE,
    current_workload_hours INTEGER DEFAULT 0 CHECK (current_workload_hours >= 0),
    max_workload_hours INTEGER DEFAULT 40,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица проектов
CREATE TABLE projects (
    id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'planned'
        CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    priority INTEGER DEFAULT 1 CHECK (priority BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estimated_start_date TIMESTAMP,
    estimated_end_date TIMESTAMP,
    actual_start_date TIMESTAMP,
    actual_end_date TIMESTAMP,
    total_estimated_hours INTEGER DEFAULT 0 CHECK (total_estimated_hours >= 0),
    total_estimated_cost INTEGER DEFAULT 0 CHECK (total_estimated_cost >= 0),
    client_name VARCHAR(255),
    client_email VARCHAR(255),

    -- Ограничения на даты
    CONSTRAINT check_estimated_dates
        CHECK (estimated_end_date IS NULL OR estimated_start_date IS NULL OR estimated_end_date >= estimated_start_date),
    CONSTRAINT check_actual_dates
        CHECK (actual_end_date IS NULL OR actual_start_date IS NULL OR actual_end_date >= actual_start_date)
);

-- Таблица задач
CREATE TABLE tasks (
    id VARCHAR(100) PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    complexity VARCHAR(50) DEFAULT 'medium'
        CHECK (complexity IN ('low', 'medium', 'high')),
    estimated_hours INTEGER CHECK (estimated_hours > 0),
    actual_hours INTEGER CHECK (actual_hours >= 0),
    required_skills TEXT[],
    dependencies TEXT[], -- ID других задач
    status VARCHAR(50) DEFAULT 'pending'
        CHECK (status IN ('pending', 'in_progress', 'completed', 'blocked', 'cancelled')),
    assigned_developer_id INTEGER REFERENCES developers(id),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Ограничения на даты
    CONSTRAINT check_task_dates
        CHECK (end_date IS NULL OR start_date IS NULL OR end_date >= start_date)
);

-- Таблица зависимостей между задачами (более структурированный подход)
CREATE TABLE task_dependencies (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(100) NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    depends_on_task_id VARCHAR(100) NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    dependency_type VARCHAR(50) DEFAULT 'finish_to_start'
        CHECK (dependency_type IN ('finish_to_start', 'start_to_start', 'finish_to_finish', 'start_to_finish')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Предотвращаем циклические зависимости на уровне БД
    CONSTRAINT no_self_dependency CHECK (task_id != depends_on_task_id),
    CONSTRAINT unique_dependency UNIQUE (task_id, depends_on_task_id)
);

-- Таблица логов изменений задач (для отслеживания прогресса)
CREATE TABLE task_logs (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(100) NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    developer_id INTEGER REFERENCES developers(id),
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    hours_logged INTEGER DEFAULT 0,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для оптимизации запросов
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_dates ON projects(estimated_start_date, estimated_end_date);
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_developer_id ON tasks(assigned_developer_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_dates ON tasks(start_date, end_date);
CREATE INDEX idx_developers_available ON developers(is_available);
CREATE INDEX idx_developers_skills ON developers USING GIN(skills);

-- Триггеры для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$ language 'plpgsql';

CREATE TRIGGER update_developers_updated_at BEFORE UPDATE ON developers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Представления для удобного просмотра данных

-- Представление для проектов с прогрессом
CREATE OR REPLACE VIEW project_progress AS
SELECT
    p.id,
    p.title,
    p.description,
    p.status,
    p.priority,
    p.estimated_start_date,
    p.estimated_end_date,
    p.actual_start_date,
    p.actual_end_date,
    p.total_estimated_hours,
    p.total_estimated_cost,
    COUNT(t.id) as total_tasks,
    COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
    COUNT(CASE WHEN t.status = 'in_progress' THEN 1 END) as in_progress_tasks,
    COUNT(CASE WHEN t.status = 'blocked' THEN 1 END) as blocked_tasks,
    ROUND(
        CASE
            WHEN COUNT(t.id) > 0 THEN
                (COUNT(CASE WHEN t.status = 'completed' THEN 1 END)::DECIMAL / COUNT(t.id)) * 100
            ELSE 0
        END, 2
    ) as progress_percent,
    SUM(COALESCE(t.actual_hours, 0)) as actual_hours_spent,
    SUM(CASE WHEN t.status = 'completed' THEN COALESCE(t.actual_hours, t.estimated_hours) ELSE 0 END) as completed_hours
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.title, p.description, p.status, p.priority,
         p.estimated_start_date, p.estimated_end_date, p.actual_start_date,
         p.actual_end_date, p.total_estimated_hours, p.total_estimated_cost;

-- Представление для загрузки разработчиков
CREATE OR REPLACE VIEW developer_workload AS
SELECT
    d.id,
    d.name,
    d.role_type,
    d.seniority,
    d.hourly_rate,
    d.is_available,
    d.current_workload_hours,
    d.max_workload_hours,
    COUNT(t.id) as active_tasks,
    SUM(CASE WHEN t.status = 'in_progress' THEN t.estimated_hours ELSE 0 END) as current_task_hours,
    COALESCE(MIN(t.start_date), CURRENT_TIMESTAMP) as next_available_date,
    CASE
        WHEN d.current_workload_hours >= d.max_workload_hours THEN 'overloaded'
        WHEN d.current_workload_hours >= d.max_workload_hours * 0.8 THEN 'busy'
        WHEN d.current_workload_hours > 0 THEN 'available'
        ELSE 'free'
    END as workload_status
FROM developers d
LEFT JOIN tasks t ON d.id = t.assigned_developer_id
    AND t.status IN ('pending', 'in_progress')
GROUP BY d.id, d.name, d.role_type, d.seniority, d.hourly_rate,
         d.is_available, d.current_workload_hours, d.max_workload_hours;

-- Функция для автоматического расчета следующего доступного времени
CREATE OR REPLACE FUNCTION get_next_available_slot(developer_id INTEGER)
RETURNS TIMESTAMP AS $
DECLARE
    last_end_date TIMESTAMP;
BEGIN
    SELECT MAX(end_date) INTO last_end_date
    FROM tasks
    WHERE assigned_developer_id = developer_id
    AND status IN ('pending', 'in_progress')
    AND end_date IS NOT NULL;

    IF last_end_date IS NULL THEN
        RETURN CURRENT_TIMESTAMP;
    ELSE
        RETURN last_end_date;
    END IF;
END;
$ LANGUAGE plpgsql;

-- Функция для проверки циклических зависимостей
CREATE OR REPLACE FUNCTION check_circular_dependency(task_id VARCHAR(100), depends_on VARCHAR(100))
RETURNS BOOLEAN AS $
DECLARE
    circular_found BOOLEAN := FALSE;
BEGIN
    -- Простая проверка на один уровень вложенности
    -- Для более сложных случаев нужна рекурсивная функция
    IF EXISTS (
        SELECT 1 FROM task_dependencies
        WHERE task_id = depends_on AND depends_on_task_id = task_id
    ) THEN
        circular_found := TRUE;
    END IF;

    RETURN circular_found;
END;
$ LANGUAGE plpgsql;

-- Начальные данные для разработчиков
INSERT INTO developers (name, role_type, hourly_rate, skills, seniority) VALUES
('Алексей Frontend Jr', 'frontend_junior', 1500, ARRAY['html', 'css', 'javascript', 'react', 'vue', 'верстка', 'адаптивный дизайн'], 'junior'),
('Мария Frontend Mid', 'frontend_middle', 2500, ARRAY['html', 'css', 'javascript', 'react', 'vue', 'typescript', 'webpack', 'оптимизация', 'тестирование'], 'middle'),
('Дмитрий Backend Jr', 'backend_junior', 1800, ARRAY['python', 'django', 'flask', 'api', 'база данных', 'sql'], 'junior'),
('Анна Backend Mid', 'backend_middle', 3000, ARRAY['python', 'django', 'flask', 'fastapi', 'postgresql', 'redis', 'celery', 'docker', 'api', 'микросервисы'], 'middle'),
('Сергей Backend Sr', 'backend_senior', 4500, ARRAY['архитектура', 'микросервисы', 'highload', 'оптимизация', 'безопасность', 'devops', 'код-ревью'], 'senior'),
('Елена Fullstack', 'fullstack_middle', 2800, ARRAY['frontend', 'backend', 'javascript', 'python', 'react', 'api', 'база данных'], 'middle'),
('Иван Дизайнер', 'ui_ux', 2200, ARRAY['дизайн', 'интерфейс', 'прототипирование', 'пользовательский опыт', 'figma', 'адобе'], 'middle'),
('Павел DevOps', 'devops', 3500, ARRAY['docker', 'kubernetes', 'ci/cd', 'aws', 'nginx', 'мониторинг', 'безопасность'], 'middle'),
('Ольга Тестировщик', 'qa_tester', 2000, ARRAY['тестирование', 'автотесты', 'selenium', 'postman', 'баг-репорты'], 'middle');

-- Комментарии к таблицам
COMMENT ON TABLE developers IS 'Таблица разработчиков и их характеристик';
COMMENT ON TABLE projects IS 'Таблица проектов';
COMMENT ON TABLE tasks IS 'Таблица задач в рамках проектов';
COMMENT ON TABLE task_dependencies IS 'Зависимости между задачами';
COMMENT ON TABLE task_logs IS 'Лог изменений задач для отслеживания прогресса';

COMMENT ON COLUMN developers.current_workload_hours IS 'Текущая загрузка разработчика в часах';
COMMENT ON COLUMN developers.max_workload_hours IS 'Максимальная недельная загрузка';
COMMENT ON COLUMN projects.priority IS 'Приоритет проекта от 1 (низкий) до 5 (критический)';
COMMENT ON COLUMN tasks.complexity IS 'Сложность задачи: low, medium, high';

-- Полезные запросы для проверки
/*
-- Просмотр всех проектов с прогрессом
SELECT * FROM project_progress ORDER BY estimated_start_date;

-- Просмотр загрузки разработчиков
SELECT * FROM developer_workload ORDER BY workload_status, name;

-- Найти свободных разработчиков с нужными навыками
SELECT d.* FROM developers d
WHERE d.is_available = TRUE
AND d.skills && ARRAY['react', 'javascript']
ORDER BY d.hourly_rate;

-- Получить очередь задач по времени
SELECT t.*, d.name as developer_name, p.title as project_title
FROM tasks t
LEFT JOIN developers d ON t.assigned_developer_id = d.id
LEFT JOIN projects p ON t.project_id = p.id
WHERE t.status IN ('pending', 'in_progress')
ORDER BY t.start_date NULLS LAST;
*/