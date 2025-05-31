import { Request } from 'express';

declare global {
  namespace Express {
    interface Request {
      user?: {
        id: number;
        username: string;
        email: string;
        company_name: string;
        is_admin: boolean;
      };
    }
  }
}