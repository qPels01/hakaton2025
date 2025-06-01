import { Router } from 'express';
import { authMiddleware } from '../middlewares/authMiddleware';
import {
  getAllForms,
  getFormById,
  createForm,
  deleteForm
} from '../controllers/formController';

const router = Router();

router.get('/', authMiddleware, getAllForms);
router.get('/:id', authMiddleware, getFormById);
router.post('/', authMiddleware, createForm);
router.delete('/:id', authMiddleware, deleteForm);

export default router;