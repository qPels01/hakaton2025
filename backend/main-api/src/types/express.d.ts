import { Request } from 'express';

declare global {
  namespace Express {
    interface Request {
      user?: {
        id: number;
        is_admin: boolean;
        username: string;
        email: string;
      };
    }
  }
}