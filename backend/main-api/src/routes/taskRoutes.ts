import { Router } from 'express';
import { authMiddleware } from '../middlewares/authMiddleware';
import {
  getAllTasks, getTaskById,
  createTask, updateTaskById, deleteTask
} from '../controllers/taskController';

const router = Router();

router.get('/', authMiddleware, getAllTasks);
router.get('/:id', authMiddleware, getTaskById);
router.post('/', authMiddleware, createTask);
router.put('/:id', authMiddleware, updateTaskById);
router.delete('/:id', authMiddleware, deleteTask);

export default router;