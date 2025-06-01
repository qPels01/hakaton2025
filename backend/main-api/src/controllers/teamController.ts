import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { Team } from '../models/Team';

const teamRepo = AppDataSource.getRepository(Team);

// Получить все команды
export async function getAllTeams(req: Request, res: Response) {
  const teams = await teamRepo.find({ relations: ['developers', 'forms'] });
  res.json(teams);
}

// Получить одну команду
export async function getTeamById(req: Request, res: Response) {
  const { id } = req.params;
  const team = await teamRepo.findOne({ where: { id: Number(id) }, relations: ['developers', 'forms'] });
  if (!team) { res.status(404).json({ message: 'Team not found' });
return}res.json(team);
}

// Создать команду (обычно только для админов)
export async function createTeam(req: Request, res: Response) {
  // Новый team может быть вообще без разработчиков
  const team = teamRepo.create();
  await teamRepo.save(team);
  res.status(201).json(team);
}

// Удалить команду (только для админов)
export async function deleteTeam(req: Request, res: Response) {
  const { id } = req.params;
  const result = await teamRepo.delete(Number(id));
  if (result.affected === 0) { res.status(404).json({ message: "Team not found" });
return;}res.json({ message: "Team deleted" });
}