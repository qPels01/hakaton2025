import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Register from "@/views/auth/Register.vue";
import Login from "@/views/auth/Login.vue";
import User from "@/views/User.vue";
import OrderForm from "@/views/form/OrderForm.vue";
import TeamLog from "@/views/TeamLog.vue";
import DevList from "@/views/DevList.vue";
import Requestions2 from "@/views/form/Requestions.vue";

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
  path: "/teams/:id",
  name: "teamLog",
  component: TeamLog,
  props: true,
},
    {
      path: "/requisition2",
      name: "requisition2",
      component: Requestions2,
    },
    {
      path: "/devlist",
      name: "devlist",
      component: DevList,
    },
  ],
});

export default router;
