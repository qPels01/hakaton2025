import { Entity, PrimaryColumn } from 'typeorm';

@Entity('task_diagram')
export class TaskDiagram {
  @PrimaryColumn('uuid')
  team_id: string;

  @PrimaryColumn()
  task_id: number;
}