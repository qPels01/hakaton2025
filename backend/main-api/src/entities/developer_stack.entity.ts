import { Entity, PrimaryColumn } from 'typeorm';

@Entity('developer_stack')
export class DeveloperStack {
  @PrimaryColumn('uuid')
  user_id: string;

  @PrimaryColumn()
  technology_id: number;
}