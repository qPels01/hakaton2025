import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Register from "@/views/Register.vue";
import Login from "@/views/Login.vue";
import User from "@/views/User.vue";
import OrderForm from "@/views/OrderForm.vue";
import Project from "@/views/Project.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/register",
      name: "register",
      component: Register,
    },
    {
      path: "/login",
      name: "login",
      component: Login,
    },
    {
      path: "/user",
      name: "user",
      component: User,
    },
    {
      path: "/order",
      name: "order",
      component: OrderForm,
    },
    {
      path: "/project",
      name: "project",
      component: Project,
    },
  ],
});

export default router;
