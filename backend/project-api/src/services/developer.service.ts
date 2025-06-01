import fs from 'fs';
import path from 'path';

const dbFile = path.resolve(__dirname, '../data/developers.json');

export async function getAllDevelopers() {
    const content = await fs.promises.readFile(dbFile, 'utf-8');
    const groups = JSON.parse(content);
    return groups.flatMap((g: any) => g.developers);
}
export async function getAllTeams() {
    const content = await fs.promises.readFile(dbFile, 'utf-8');
    const teams = JSON.parse(content);
    return teams;
}