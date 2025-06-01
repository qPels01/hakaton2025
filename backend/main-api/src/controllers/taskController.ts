import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { Task } from '../models/Task';
import { Developer } from '../models/Developer';
import { Form } from '../models/Form';

const taskRepo = AppDataSource.getRepository(Task);
const formRepo = AppDataSource.getRepository(Form);
const developerRepo = AppDataSource.getRepository(Developer);

export async function getAllTasks(req: Request, res: Response) {
  const tasks = await taskRepo.find({ relations: ['form', 'developer'] });
  res.json(tasks);
}

export async function getTaskById(req: Request, res: Response) {
  const { id } = req.params;
  const task = await taskRepo.findOne({ where: { id: Number(id) }, relations: ['developer', 'form'] });
  if (!task) { res.status(404).json({ message: 'Task not found' });return;}
  res.json(task);
}

export async function createTask(req: Request, res: Response) {
  /**
   * {
   *   form_id: number,
   *   developer_id?: number,
   *   name: string,
   *   hours: number,
   *   deadline: string (date),
   *   is_completed: boolean
   * }
   */
  const { form_id, developer_id, name, hours, deadline, is_completed } = req.body;
  const form = await formRepo.findOne({ where: { id: form_id } });
  if (!form) { res.status(400).json({ message: "Form not found" });
  return;}
  let developer = undefined;
  if (developer_id) {
    developer = await developerRepo.findOne({ where: { id: developer_id } });
    if (!developer) { res.status(400).json({ message: "Developer not found" });
    return;}}

  const task = taskRepo.create({
    form,
    developer,
    name,
    hours,
    deadline,
    is_completed: !!is_completed
  });

  await taskRepo.save(task);
  res.status(201).json(task);
}

export async function updateTaskById(req: Request, res: Response) {
  const { id } = req.params;
  const { developer_id, name, hours, deadline, is_completed } = req.body;
  const task = await taskRepo.findOne({ where: { id: Number(id) } });

  if (!task) { res.status(404).json({ message: 'Task not found' });
  return;}
  if (developer_id !== undefined) {
    const developer = await developerRepo.findOne({ where: { id: developer_id } });
    if (!developer) { res.status(400).json({ message: "Developer not found" });
  return;}task.developer = developer;
  }
  task.name = name ?? task.name;
  task.hours = hours ?? task.hours;
  task.deadline = deadline ?? task.deadline;
  task.is_completed = is_completed ?? task.is_completed;

  await taskRepo.save(task);
  res.json(task);
}

export async function deleteTask(req: Request, res: Response) {
  const { id } = req.params;
  const result = await taskRepo.delete(Number(id));
  if (result.affected === 0) { res.status(404).json({ message: 'Task not found' });
return;}res.json({ message: 'Task deleted' });
}