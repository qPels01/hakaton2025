import { Entity, PrimaryGeneratedColumn, OneToMany, ManyToOne, JoinColumn, Column } from "typeorm";
import { Developer } from "./Developer";
import { Form } from "./Form";
import { User } from "./User";

@Entity('teams')
export class Team {
    @PrimaryGeneratedColumn()
    id: number;

    @OneToMany(() => Developer, developer => developer.team)
    developers: Developer[];

    @OneToMany(() => Form, form => form.team)
    forms: Form[];
}