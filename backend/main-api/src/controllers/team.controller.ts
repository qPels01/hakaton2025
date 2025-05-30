import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { Team } from "../entities/team.entity";

const teamRepo = AppDataSource.getRepository(Team);

export const getTeams = async (req: Request, res: Response) => {
  const teams = await teamRepo.find({ relations: ["users"] });
  res.json(teams);
};

export const createTeam = async (req: Request, res: Response) => {
  const { team_name } = req.body;
  const team = teamRepo.create({ team_name });
  await teamRepo.save(team);
  res.status(201).json(team);
};

export const getTeamById = async (req: Request, res: Response) => {
  const team = await teamRepo.findOne({
    where: { team_id: req.params.id },
    relations: ["users"],
  });
  if (!team) res.status(404).json({ message: "Not found" });
  res.json(team);
};

export const updateTeam = async (req: Request, res: Response) => {
  const { team_name } = req.body;
  const team = await teamRepo.findOneBy({ team_id: req.params.id });
  if (!team) res.status(404).json({ message: "Not found" });
  team.team_name = team_name;
  await teamRepo.save(team);
  res.json(team);
};

export const deleteTeam = async (req: Request, res: Response) => {
  const team = await teamRepo.findOneBy({ team_id: req.params.id });
  if (!team) res.status(404).json({ message: "Not found" });
  await teamRepo.remove(team);
  res.status(204).send();
};