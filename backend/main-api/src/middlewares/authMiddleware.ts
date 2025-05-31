import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';


export function authMiddleware(req: Request, res: Response, next: NextFunction): void {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer '))
{
    res.status(401).json({ message: 'No token provided' });
return
}
  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret');
    req.user = decoded as {
      id: number;
      username: string;
      email: string;
      company_name: string;
      is_admin: boolean;
    };
    next();
  } catch {
    res.status(401).json({ message: 'Invalid or expired token' });
    return
}
}