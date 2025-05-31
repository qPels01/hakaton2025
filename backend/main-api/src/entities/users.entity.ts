// users.entity.ts
import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToOne, JoinColumn } from 'typeorm';
import { Team } from './teams.entity';
import { UserData } from './user_data.entity';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  user_id: string;

  @Column()
  role: string;

  @Column()
  email: string;

  @Column()
  password: string;

  @ManyToOne(() => Team, team => team.users, { nullable: true })
  @JoinColumn({ name: 'team_id' })
  team: Team;

  @OneToOne(() => UserData, userData => userData.user, { cascade: true })
  userData: UserData;
}