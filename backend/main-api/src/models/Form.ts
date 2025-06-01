import {
    Entity, PrimaryGeneratedColumn, Column,
    ManyToOne, JoinColumn, OneToMany, CreateDateColumn
} from "typeorm";
import { Team } from "./Team";
import { Task } from "./Task";
import { User } from "./User";

@Entity('forms')
export class Form {
    @PrimaryGeneratedColumn()
    id: number;

    @Column({ length: 200 })
    title: string;

    @ManyToOne(() => Team, team => team.forms, { onDelete: "CASCADE" })
    @JoinColumn({ name: "team_id" })
    team: Team;

    @Column()
    deadline: Date;

    @Column({ type: "numeric", precision: 15, scale: 2, nullable: true })
    total_cost: number;

    @CreateDateColumn({ type: "timestamp" })
    created_at: Date;

    @OneToMany(() => Task, task => task.form)
    tasks: Task[];

    @ManyToOne(() => User, { nullable: false, onDelete: "CASCADE" })
    @JoinColumn({ name: "user_id" })
    user: User;

    @Column()
    user_id: number;
}