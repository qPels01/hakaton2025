import { Entity, PrimaryColumn } from 'typeorm';

@Entity('task_technology')
export class TaskTechnology {
  @PrimaryColumn()
  technology_id: number;

  @PrimaryColumn()
  task_id: number;
}