import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import RegisterPage from "@/views/Register.vue";

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
      component: RegisterPage,
    },
  ],
});

export default router;
