import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { Developer } from '../models/Developer';
import { Team } from '../models/Team';

const developerRepo = AppDataSource.getRepository(Developer);
const teamRepo = AppDataSource.getRepository(Team);

export async function getAllDevelopers(req: Request, res: Response) {
  const developers = await developerRepo.find({ relations: ['team'] });
  res.json(developers);
}

export async function getDeveloperById(req: Request, res: Response) {
  const { id } = req.params;
  const developer = await developerRepo.findOne({ where: { id: Number(id) }, relations: ['team'] });
  if (!developer) { res.status(404).json({ message: 'Developer not found' });
return;}res.json(developer);
}

export async function createDeveloper(req: Request, res: Response) {
  /**
   * {
   *   name: string,
   *   role: string,
   *   level: string,
   *   hourly_rate_rub: number,
   *   skills: string[],
   *   team_id: number
   * }
   */
  const { name, role, level, hourly_rate_rub, skills, team_id } = req.body;

  let team = undefined;
  if (team_id) {
    team = await teamRepo.findOne({ where: { id: team_id } });
    if (!team) { res.status(400).json({ message: "Team not found" });
    return}}

  const developer = developerRepo.create({
    name,
    role,
    level,
    hourly_rate_rub,
    skills,
    team
  });

  await developerRepo.save(developer);
  res.status(201).json(developer);
}

export async function updateDeveloperById(req: Request, res: Response) {
  const { id } = req.params;
  const { name, role, level, hourly_rate_rub, skills, team_id } = req.body;
  const developer = await developerRepo.findOne({ where: { id: Number(id) } });
  if (!developer) { res.status(404).json({ message: 'Developer not found' });
return;}
  if (team_id !== undefined) {
    const team = await teamRepo.findOne({ where: { id: team_id } });
    if (!team){ res.status(400).json({ message: "Team not found" });
  return;}developer.team = team;
  }

  developer.name = name ?? developer.name;
  developer.role = role ?? developer.role;
  developer.level = level ?? developer.level;
  developer.hourly_rate_rub = hourly_rate_rub ?? developer.hourly_rate_rub;
  developer.skills = skills ?? developer.skills;

  await developerRepo.save(developer);
  res.json(developer);
}

export async function deleteDeveloper(req: Request, res: Response) {
  const { id } = req.params;
  const result = await developerRepo.delete(Number(id));
  if (result.affected === 0) { res.status(404).json({ message: 'Developer not found' });
return;}res.json({ message: 'Developer deleted' });
}