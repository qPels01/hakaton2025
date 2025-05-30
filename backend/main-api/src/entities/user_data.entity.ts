import { Entity, PrimaryColumn, Column, OneToOne, JoinColumn } from 'typeorm';
import { User } from './user.entity';

@Entity('user_data')
export class UserData {
  @PrimaryColumn('uuid')
  user_id: string;

  @Column()
  company_name: string;

  @Column()
  first_name: string;

  @Column()
  last_name: string;

  @OneToOne(() => User, user => user.userData)
  @JoinColumn({ name: 'user_id' })
  user: User;
}