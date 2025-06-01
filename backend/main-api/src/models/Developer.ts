import {
    Entity, PrimaryGeneratedColumn, Column,
    ManyToOne, JoinColumn
} from "typeorm";
import { Team } from "./Team";

@Entity('developers')
export class Developer {
    @PrimaryGeneratedColumn()
    id: number;

    @Column({ length: 100 })
    name: string;

    @Column({ length: 50 })
    role: string;

    @Column({ length: 50 })
    level: string;

    @Column({ type: "numeric", precision: 10, scale: 2 })
    hourly_rate_rub: number;

    @Column("text", { array: true })
    skills: string[];

    @ManyToOne(() => Team, team => team.developers, { nullable: true, onDelete: "SET NULL" })
    @JoinColumn({ name: "team_id" })
    team: Team;
}