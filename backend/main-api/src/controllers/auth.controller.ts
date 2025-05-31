// src/controllers/auth.controller.ts
import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { User } from "../entities/users.entity";
import { Team } from "../entities/teams.entity";
import { UserData } from "../entities/user_data.entity";
import bcrypt from "bcrypt";

const userRepo = AppDataSource.getRepository(User);
const teamRepo = AppDataSource.getRepository(Team);
const userDataRepo = AppDataSource.getRepository(UserData);

export const register = async (req: Request, res: Response): Promise<void> => {
  try {
    const { email, password, role, team_id } = req.body;

    const existing = await userRepo.findOneBy({ email });
    if (existing) {
      res.status(409).json({ message: "Такой email уже зарегистрирован" });
      return;
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    let team = null;
    if (team_id) {
      team = await teamRepo.findOneBy({ team_id: team_id });
      if (!team) {
        res.status(400).json({ message: "Указанная команда не найдена" });
        return;
      }
    }

    // Создаём UserData (или просто пустую запись, если данных нет)
    const userData = userDataRepo.create({
      company_name: "",  // или req.body.company_name
      first_name: "",
      last_name: "",
      // user будет подставлен ниже TypeORM'ом через отношение
    });

    // Создаём пользователя и связываем с userData
    const user = userRepo.create({
        email,
        password: hashedPassword,
        role: role || "user",
        team: team || null,
        userData
    });

    await userRepo.save(user); // должно автоматом создать обе записи благодаря cascade

    // Если хотите, верните только безопасные поля:
    const { password: _, ...safeUser } = user;
    res.status(201).json(safeUser);

  } catch (error) {
    console.error("Ошибка при регистрации пользователя:", error);
    res.status(500).json({ message: "Ошибка сервера" });
  }
};