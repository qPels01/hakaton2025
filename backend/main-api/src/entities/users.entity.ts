import { Entity, PrimaryGeneratedColumn, Column, OneToOne, JoinColumn, ManyToMany, JoinTable } from 'typeorm';
import { UserData } from './user_data.entity';
import { Team } from './team.entity';

@Entity('users')
export class Users {
  @PrimaryGeneratedColumn('uuid')
  user_id: string;

  @Column()
  role: string;

  @Column()
  email: string;

  @Column()
  password: string;

  @OneToOne(() => UserData, userData => userData.user, { cascade: true })
  userData: UserData;

  @ManyToMany(() => Team, team => team.users)
  teams: Team[];
}