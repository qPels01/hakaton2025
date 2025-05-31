<template>
  <div class="user-info" v-if="userInfo">
    <h1>Имя пользователя: {{ userInfo.username }}</h1>
  </div>
  <div class="admin-panel" v-if="userInfo && isManager">
    <button class="admin-button" v-if="isManager">Посмотреть заявки</button>
    <button class="admin-button" v-if="isManager">Список разработчиков</button>
    <button @click="toOrderForm" v-if="userInfo">Cделать заказ</button>
  </div>
  <Diagramm v-if="userInfo" />
  <div class="logout">
    <h1>Выйти из аккаунта</h1>
    <button @click="logout" v-if="userInfo">Выйти</button>
  </div>
</template>

<script lang="ts">
import Diagramm from "@/components/Diagramm.vue";
import api from "@/api/axios";
import { jwtDecode } from "jwt-decode";

interface DecodedToken {
  username: string;
  email: string;
  is_admin?: boolean;
  [key: string]: any;
}

export default {
  name: "user",
  components: { Diagramm },
  data() {
    return {
      userInfo: null as DecodedToken | null,
      error: "",
    };
  },
  computed: {
    isManager(): boolean {
      return !!!(this.userInfo && this.userInfo.is_admin);
    },
  },
  methods: {
    toOrderForm() {
      this.$router.push("/order");
    },
    logout() {
      localStorage.removeItem("jwt_token");
      window.dispatchEvent(new Event("storage"));
      this.$router.push("/login");
    },
    getUserFromToken() {
      const token = localStorage.getItem("jwt_token");
      if (!token) return null;
      try {
        // Используем jwt-decode для декодирования payload токена
        return jwtDecode<DecodedToken>(token);
      } catch (e) {
        // Если токен битый — удаляем, редиректим на логин
        localStorage.removeItem("jwt_token");
        this.$router.push("/login");
        return null;
      }
    },
  },
  async mounted() {
    this.userInfo = this.getUserFromToken();
    if (!this.userInfo) {
      this.$router.push("/login");
      return;
    }
    // Валидация токена на сервере (например, если токен отозван)
    try {
      const res = await api.get("/user/protected");
      if (res.data.user) {
        // Можно профрешить userInfo — например, если на сервере данные изменились.
        this.userInfo = { ...this.userInfo, ...res.data.user };
      }
    } catch (err) {
      if (err.response && err.response.status === 401) {
        localStorage.removeItem("jwt_token");
        this.$router.push("/login");
      } else {
        this.error = "Ошибка получения данных пользователя";
      }
    }
  },
};
</script>

<style scoped>
.user-info {
  display: block;
  background: #42464e;
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 80%;
  margin: 2rem auto;
}
.admin-panel {
  display: flex;
  align-items: center;
  background: #42464e;
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 80%;
  margin: 2rem auto;
  gap: 2rem;
}
.logout {
  padding: 2rem;
  margin: 2rem auto;
}
.admin-button {
  background: rgb(246, 137, 38);
}
.admin-button:hover {
  background: rgb(200, 112, 29);
}
</style>
