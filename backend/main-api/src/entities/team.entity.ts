import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from "typeorm";
import { User } from "./user.entity";

@Entity("teams")
export class Team {
  @PrimaryGeneratedColumn("uuid")
  team_id: string;

  @Column()
  team_name: string;

  // Связь: Одна команда — Многие пользователи
  @OneToMany(() => User, user => user.team)
  users: User[];
}