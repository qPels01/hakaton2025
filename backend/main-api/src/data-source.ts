import { DataSource } from "typeorm";
import { DeveloperStack } from "./entities/developer_stack.entity";
import { TaskDiagram } from "./entities/task_diagram.entity";
import { TaskTechnology } from "./entities/task_technology.entity";
import { Task } from "./entities/tasks.entity";
import { Team } from "./entities/teams.entity";
import { Technology } from "./entities/technology.entity";
import { UserData } from "./entities/user_data.entity";
import { User } from "./entities/users.entity";


export const AppDataSource = new DataSource({
  type: "postgres",
  host: process.env.POSTGRES_HOST,
  port: Number(process.env.POSTGRES_PORT),
  username: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  database: process.env.POSTGRES_DB,
  entities: [User, DeveloperStack, TaskDiagram, TaskTechnology, Task, Team, Technology, UserData],
  synchronize: true,
  logging: false,
});