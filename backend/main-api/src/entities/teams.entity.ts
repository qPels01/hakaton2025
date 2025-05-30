import { Entity, PrimaryGeneratedColumn, Column, ManyToMany, JoinTable } from 'typeorm';
import { User } from './user.entity';

@Entity('teams')
export class Teams {
  @PrimaryGeneratedColumn('uuid')
  team_id: string;

  @Column()
  team_name: string;

  @ManyToMany(() => User, user => user.team)
  @JoinTable({
    name: 'team',
    joinColumn: { name: 'team_id', referencedColumnName: 'team_id' },
    inverseJoinColumn: { name: 'user_id', referencedColumnName: 'user_id' }
  })
  users: User[];
}