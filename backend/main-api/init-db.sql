-- 1. Пользователи
CREATE TABLE users (
    user_id      UUID PRIMARY KEY,
    role         VARCHAR NOT NULL,
    email        VARCHAR UNIQUE NOT NULL,
    password     VARCHAR NOT NULL
);

-- 2. Доп. инфа о пользователе
CREATE TABLE user_data (
    user_id      UUID PRIMARY KEY REFERENCES users(user_id),
    company_name VARCHAR,
    first_name   VARCHAR,
    last_name    VARCHAR
);

-- 3. Команды
CREATE TABLE teams (
    team_id      UUID PRIMARY KEY,
    team_name    VARCHAR NOT NULL
);

-- 4. Таблица связи "пользователь-команда"
CREATE TABLE team (
    team_id      UUID REFERENCES teams(team_id),
    user_id      UUID REFERENCES users(user_id),
    PRIMARY KEY (team_id, user_id)
);

-- 5. Технологии
CREATE TABLE technology (
    technology_id   SERIAL PRIMARY KEY,
    technology_name VARCHAR NOT NULL UNIQUE
);

-- 6. Cвязь "разработчик-стек"
CREATE TABLE developer_stack (
    user_id        UUID REFERENCES users(user_id),
    technology_id  INTEGER REFERENCES technology(technology_id),
    PRIMARY KEY (user_id, technology_id)
);

-- 7. Задачи
CREATE TABLE tasks (
    task_id         SERIAL PRIMARY KEY,
    task_description TEXT NOT NULL,
    task_type        VARCHAR NOT NULL,
    user_id         UUID REFERENCES users(user_id),
    task_start      TIMESTAMP,
    task_end        TIMESTAMP
);

-- 8. Диаграмма задач (связь задача-команда)
CREATE TABLE task_diagram (
    team_id   UUID REFERENCES teams(team_id),
    task_id   INTEGER REFERENCES tasks(task_id),
    PRIMARY KEY (team_id, task_id)
);

-- 9. Технологии задач
CREATE TABLE task_technology (
    technology_id INTEGER REFERENCES technology(technology_id),
    task_id       INTEGER REFERENCES tasks(task_id),
    PRIMARY KEY (technology_id, task_id)
);