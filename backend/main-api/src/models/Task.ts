import {
    Entity, PrimaryGeneratedColumn, Column,
    ManyToOne, JoinColumn
} from "typeorm";
import { Developer } from "./Developer";
import { Form } from "./Form";

@Entity('tasks')
export class Task {
    @PrimaryGeneratedColumn()
    id: number;

    @ManyToOne(() => Developer, developer => developer.id, { onDelete: "CASCADE" })
    @JoinColumn({ name: "dev_id" })
    developer: Developer;

    @ManyToOne(() => Form, form => form.tasks, { onDelete: "CASCADE" })
    @JoinColumn({ name: "form_id" })
    form: Form;

    @Column({ length: 200 })
    name: string;

    @Column({ type: "numeric", precision: 7, scale: 2 })
    hours: number;

    @Column()
    deadline: Date;

    @Column({ default: false })
    is_completed: boolean;
}