import { DataSource } from "typeorm";
import { User } from "./models/User";
import { Team } from "./models/Team";
import { Developer } from "./models/Developer";
import { Task } from "./models/Task";
import { Form } from "./models/Form";


export const AppDataSource = new DataSource({
  type: "postgres",
  host: process.env.POSTGRES_HOST,
  port: Number(process.env.POSTGRES_PORT),
  username: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  database: process.env.POSTGRES_DB,
  entities: [User, Team, Developer, Task, Form],
  synchronize: true,
  logging: false,
});
