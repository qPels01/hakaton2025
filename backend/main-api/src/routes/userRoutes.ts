import { Router } from 'express';
import { getAllUsers, getUserById, updateUserById, deleteUser } from '../controllers/userController';
import { authMiddleware } from '../middlewares/authMiddleware';
import { adminMiddleware } from "../middlewares/adminMiddleware";

const router = Router();

router.get('/', authMiddleware, getAllUsers);
router.get('/:id', authMiddleware, getUserById);
router.put('/:id', authMiddleware, updateUserById);
router.delete('/:id', authMiddleware, deleteUser);

export default router;