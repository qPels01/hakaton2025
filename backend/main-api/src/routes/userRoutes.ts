import { Router } from 'express';
import { authMiddleware } from '../middlewares/authMiddleware';

const router = Router();

router.get('/protected', authMiddleware, (req, res) => {
  const user = req.user;
  res.json({ message: 'You are authorized!', user });
});

export default router;
