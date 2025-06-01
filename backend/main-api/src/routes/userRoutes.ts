import { Router } from 'express';
import { getAllUsers, getUserById, updateUserById, deleteUser } from '../controllers/userController';
import { authMiddleware } from '../middlewares/authMiddleware';
import { adminMiddleware } from "../middlewares/adminMiddleware";

const router = Router();

// router.get('/', authMiddleware, getAllUsers);
// router.get('/:id', authMiddleware, getUserById);
// router.put('/:id', authMiddleware, updateUserById);
// router.delete('/:id', authMiddleware, deleteUser);
router.get('/protected', authMiddleware, (req, res) => {
  const user = req.user;
  res.json({ message: 'You are authorized!', user });
});
export default router;