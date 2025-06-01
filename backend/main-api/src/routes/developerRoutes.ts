import { Router } from 'express';
import { authMiddleware } from '../middlewares/authMiddleware';
import {
  getAllDevelopers,
  getDeveloperById,
  createDeveloper,
  updateDeveloperById,
  deleteDeveloper
} from '../controllers/developerController';

const router = Router();

router.get('/', authMiddleware, getAllDevelopers);
router.get('/:id', authMiddleware, getDeveloperById);
router.post('/', authMiddleware, createDeveloper);
router.put('/:id', authMiddleware, updateDeveloperById);
router.delete('/:id', authMiddleware, deleteDeveloper);

export default router;