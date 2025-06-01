import * as dotenv from 'dotenv';
import * as path from "path";
dotenv.config({ path: path.resolve(__dirname, "../../.env") });

import "reflect-metadata";
import { AppDataSource } from '../data-source';
import { Developer } from '../models/Developer';
import { Task } from '../models/Task';
import { Form } from '../models/Form';
import { Team } from '../models/Team';

const ROLES = ["frontend", "backend", "qa", "designer"] as const;
const LEVELS = ["junior", "middle", "senior"] as const;

function getRandomInt(min: number, max: number) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomSkills() {
  const allSkills = [
    "React", "Angular", "Vue", "Node.js", "Python", "Java", "Kotlin", "Figma", "Jest",
    "Selenium", "Photoshop", "CSS", "HTML", "PostgreSQL", "MongoDB", "TypeScript"
  ];
  // 2-5 уникальных скилла
  const count = getRandomInt(2, 5);
  return allSkills
    .sort(() => 0.5 - Math.random())
    .slice(0, count);
}

function getRandomName(role: string, level: string, idx: number): string {
  // Можно улучшить: использовать faker-js, но для простоты:
  return `${role}_${level}_${Math.floor(Math.random() * 1000) + idx}`;
}

async function seed() {
  await AppDataSource.initialize();

  // Удаляем старые команды и девелоперов (ОСТОРОЖНО)
await AppDataSource.getRepository(Task).createQueryBuilder().delete().execute();
await AppDataSource.getRepository(Form).createQueryBuilder().delete().execute();
await AppDataSource.getRepository(Developer).createQueryBuilder().delete().execute();
await AppDataSource.getRepository(Team).createQueryBuilder().delete().execute();

  for (let i = 1; i <= 10; i++) {
    const teamRepo = AppDataSource.getRepository(Team);
    const devRepo = AppDataSource.getRepository(Developer);

    // Создаем новую команду
    const team = teamRepo.create(); // нет имени! Если нужен name: team = teamRepo.create({ name: ... });
    await teamRepo.save(team);

    const devCount = getRandomInt(2, 5);
    for (let j = 0; j < devCount; j++) {
      const role = ROLES[getRandomInt(0, ROLES.length - 1)];
      const level = LEVELS[getRandomInt(0, LEVELS.length - 1)];
      const name = getRandomName(role, level, i * 100 + j);
      const developer = devRepo.create({
        name,
        role,
        level,
        hourly_rate_rub: getRandomInt(1500, 5000),
        skills: getRandomSkills(),
        team: team
      });
      await devRepo.save(developer);
    }

    console.log(`Создана команда ${team.id} с ${devCount} разработчиками`);
  }

  await AppDataSource.destroy();
  console.log("Наполнение завершено!");
}

seed().catch(e => {
  console.error(e);
  process.exit(1);
});