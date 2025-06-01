import { Entity, PrimaryGeneratedColumn, OneToMany, ManyToOne, JoinColumn, Column } from "typeorm";
import { Developer } from "./Developer";
import { Form } from "./Form";
import { User } from "./User";

@Entity('teams')
export class Team {
    @PrimaryGeneratedColumn()
    id: number;

    // Связь с Users: каждая команда создана каким-то пользователем
    @ManyToOne(() => User, { nullable: false, onDelete: "CASCADE" })
    @JoinColumn({ name: "user_id" })
    user: User;

    // Можно явно обозначать user_id если хочется вручную получать id без подгрузки user
    @Column()
    user_id: number;

    @OneToMany(() => Developer, developer => developer.team)
    developers: Developer[];

    @OneToMany(() => Form, form => form.team)
    forms: Form[];
}