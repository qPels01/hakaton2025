import { Entity, PrimaryGeneratedColumn, Column, ManyToOne, OneToOne, JoinColumn } from "typeorm";
import { Team } from "./team.entity";
import { UserData } from "./user_data.entity";

@Entity("users")
export class User {
  @PrimaryGeneratedColumn("uuid")
  user_id: string;

  @Column()
  role: string;

  @Column({ unique: true })
  email: string;

  @Column()
  password: string;

  @ManyToOne(() => Team, team => team.users)
  @JoinColumn({ name: "team_id" })
  team: Team;

  @OneToOne(() => UserData, userData => userData.user, { cascade: true })
  @JoinColumn({ name: "user_id" })
  userData: UserData;
}