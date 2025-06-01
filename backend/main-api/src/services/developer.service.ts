// src/services/developer.service.ts

import { AppDataSource } from '../data-source';
import { Developer } from '../models/Developer';
import { Team } from '../models/Team';

export async function getAllDevelopers() {
    const repo = AppDataSource.getRepository(Developer);
    return await repo.find({ relations: ['team'] });
}

export async function getAllTeams() {
    const repo = AppDataSource.getRepository(Team);
    return await repo.find({ relations: ['developers'] });
}

export async function getAllTeamsMapped() {
    const teams = await getAllTeams();
    return teams.map(team => ({ [team.id]: team.developers }));
}