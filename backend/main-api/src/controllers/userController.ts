import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { User } from '../models/User';

const userRepo = AppDataSource.getRepository(User);

export async function getAllUsers(req: Request, res: Response) {
  const users = await userRepo.find({ select: ["id", "username", "email", "is_admin", "company_name", "created_at"] });
  res.json(users);
}

export async function getUserById(req: Request, res: Response) {
  const { id } = req.params;
  const user = await userRepo.findOne({ where: { id: Number(id) } });
  if (!user) {res.status(404).json({ message: "User not found" });
    return;
}
  res.json(user);
}

export async function updateUserById(req: Request, res: Response) {
  const { id } = req.params;
  const { email, company_name } = req.body;
  let user = await userRepo.findOne({ where: { id: Number(id) } });
  if (!user) {res.status(404).json({ message: "User not found" });return;}
  user.email = email ?? user.email;
  user.company_name = company_name ?? user.company_name;
  await userRepo.save(user);
  res.json(user);
}

export async function deleteUser(req: Request, res: Response) {
  const { id } = req.params;
  const result = await userRepo.delete(Number(id));
  if (result.affected === 0) { res.status(404).json({ message: "User not found" });return;}
  res.json({ message: "User deleted" });
}