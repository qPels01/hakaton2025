// teams.entity.ts
import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import { User } from './users.entity';

@Entity('teams')
export class Team {
  @PrimaryGeneratedColumn('uuid')
  team_id: string;

  @Column()
  team_name: string;

  @OneToMany(() => User, user => user.team)
  users: User[];
}