import { Request, Response } from 'express';
import { AppDataSource } from '../data-source';
import { Form } from '../models/Form';
import { Task } from '../models/Task';
import { Team } from '../models/Team';
import { User } from '../models/User';

const formRepo = AppDataSource.getRepository(Form);
const teamRepo = AppDataSource.getRepository(Team);
const userRepo = AppDataSource.getRepository(User);
const taskRepo = AppDataSource.getRepository(Task);

export async function getAllForms(req: Request, res: Response) {
  const forms = await formRepo.find({
    relations: ["team", "tasks", "user"],
    order: { created_at: "DESC" }
  });
  res.json(forms);
}

export async function getFormById(req: Request, res: Response) {
  const { id } = req.params;
  const form = await formRepo.findOne({ where: { id: Number(id) }, relations: ["team", "tasks", "user"] });
  if (!form) {res.status(404).json({ message: "Form not found" });
return;}
  res.json(form);
}

export async function createForm(req: Request, res: Response) {

  const { title, team_id, deadline, total_cost, tasks = [] } = req.body;
  const user_id = req.user!.id;

  const team = await teamRepo.findOne({ where: { id: team_id } });
  if (!team){ res.status(400).json({ message: "No such team" });
  return;}
  let form = formRepo.create({
    title,
    team,
    deadline: new Date(deadline),
    total_cost: total_cost,
    user_id,
    user: await userRepo.findOneBy({ id: user_id }),
  });
  await formRepo.save(form);

  if (tasks && Array.isArray(tasks)) {
    const newTasks: Task[] = [];
    for (const t of tasks) {
      const task = taskRepo.create({
        name: t.name,
        developer: t.developer_id ? { id: t.developer_id } : undefined,
        form,
        hours: t.hours,
        deadline: t.deadline,
        is_completed: false
      });
      await taskRepo.save(task);
      newTasks.push(task);
    }
    form.tasks = newTasks;
  }

  form = await formRepo.findOne({ where: { id: form.id }, relations: ["team", "tasks", "user"] });
  res.status(201).json(form);
}

export async function deleteForm(req: Request, res: Response) {
  const { id } = req.params;
  const result = await formRepo.delete(Number(id));
  if (result.affected === 0) { res.status(404).json({ message: "Form not found" });
return;}res.json({ message: "Form deleted" });
}
