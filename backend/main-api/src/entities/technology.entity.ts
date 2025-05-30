import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity('technology')
export class Technology {
  @PrimaryGeneratedColumn()
  technology_id: number;

  @Column()
  technology_name: string;
}