import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { User } from '../entities/users.entity';
import { Team } from '../entities/teams.entity';

const userRepo = AppDataSource.getRepository(User);
const teamRepo = AppDataSource.getRepository(Team);

export const getUsers = async (req: Request, res: Response) => {
  try {
    const users = await userRepo.find({ relations: ['team'] });
    res.json(users); // просто вызываем!
  } catch (e) {
    res.status(500).json({ message: "Server error" });
  }
};

export const createUser = async (req: Request, res: Response): Promise<void>  => {
  try {
    const { role, email, password, team_id } = req.body;
    let team = null;
    if (team_id) {
      team = await teamRepo.findOneBy({ team_id });
      if (!team) {res.status(400).json({ message: 'Team not found' });
        return 
      }
    }
    const user = userRepo.create({
      role,
      email,
      password,
      team
    });
    await userRepo.save(user);
    res.status(201).json(user);
  } catch (e) {
    res.status(500).json({ message: "Server error" });
  }
};

export const assignTeam = async (req: Request, res: Response): Promise<void>  => {
  try {
    const { userId } = req.params;
    const { team_id } = req.body;
    const user = await userRepo.findOne({
      where: { user_id: userId },
      relations: ['team']
    });

    if (!user) {res.status(404).json({ message: 'User not found' });
 return ;
}

    const team = await teamRepo.findOneBy({ team_id });
    if (!team) {res.status(404).json({ message: 'Team not found' });
     return ;
}

    user.team = team;
    await userRepo.save(user);

    res.json(user);
  } catch (e) {
    res.status(500).json({ message: "Server error" });
  }
};