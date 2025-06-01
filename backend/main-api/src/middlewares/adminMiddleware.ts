import { Request, Response, NextFunction } from "express";

export function adminMiddleware(req: Request, res: Response, next: NextFunction) {
  if (!req.user) {
     res.status(401).json({ message: "Unauthorized (not authenticated)" });
    return;
    }
  if (!req.user.is_admin) {
    res.status(403).json({ message: "Admin privileges required" });
    return;
}
  next();
}