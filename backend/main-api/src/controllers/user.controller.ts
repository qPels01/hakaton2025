import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { User } from '../entities/user.entity';

const userRepo = AppDataSource.getRepository(User);

export const getUsers = async (req: Request, res: Response) => {
  const users = await userRepo.find({
    relations: ['team']
  });
  res.json(users);
};

export const createUser = async (req: Request, res: Response) => {
  const { role, email, password, team_id } = req.body;
  const user = userRepo.create({ role, email, password, team: { team_id } });
  await userRepo.save(user);
  res.status(201).json(user);
};

export const assignTeam = async (req: Request, res: Response) => {
  const { userId } = req.params;
  const { team_id } = req.body;
  const user = await userRepo.findOneByOrFail({ user_id: userId });
  user.team = { team_id } as any;
  await userRepo.save(user);
  res.json(user);
};