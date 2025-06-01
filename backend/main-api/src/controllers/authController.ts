import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { User } from '../models/User';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';

const userRepo = AppDataSource.getRepository(User);

export const register = async (req: Request, res: Response): Promise<void> => {
  const { username, email, company_name, password, is_admin } = req.body;

  if (!username || !email || !password) {
    res.status(400).json({ message: 'username, email, and password are required' });
    return
  }

  try {
    const existingUser = await userRepo.findOne({ where: [{ username }, { email }] });
    if (existingUser) {
      res.status(409).json({ message: 'User with this username or email already exists' });
      return
    }

    const hashedPassword = await bcrypt.hash(password, 10);
    const user = userRepo.create({
      username,
      email,
      company_name: company_name || null,
      hash_password: hashedPassword,
      is_admin: false,
    });
    const token = jwt.sign(
      { 
        id: user.id,
        is_admin: user.is_admin,
        username: user.username,
        email: user.email,
        company_name: user.company_name
      },
      process.env.JWT_SECRET || 'secret',
      { expiresIn: '365d' }
    );
    await userRepo.save(user);
     res.status(201).json({ message: 'User registered successfully',token });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Registration failed' });
  }
};

export const login = async (req: Request, res: Response): Promise<void> => {
  const { username, password } = req.body;

  if (!username || !password){
    res.status(400).json({ message: 'username and password are required' });
    return
}

  try {
    const user = await userRepo.findOne({ where: { username } });

    if (!user){
        res.status(401).json({ message: 'Invalid username or password' });
        return
    }

    const isMatch = await bcrypt.compare(password, user.hash_password);

    if (!isMatch)
    {
        res.status(401).json({ message: 'Invalid username or password' });
        return
    }
    const token = jwt.sign(
      { 
        id: user.id,
        is_admin: user.is_admin,
        username: user.username,
        email: user.email,
        company_name: user.company_name
      },
      process.env.JWT_SECRET || 'secret',
      { expiresIn: '365d' }
    );

    res.json({ token });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Login failed' });
  }
};
