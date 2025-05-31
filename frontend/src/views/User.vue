<template>
  <div class="user-info">
    <h1>Имя пользователя: Иван Иванов Иванович</h1>
  </div>
  <div class="admin-panel">
    <button class="admin-button" v-if="isManager">Посмотреть заявки</button>
    <button class="admin-button" v-if="isManager">Список разработчиков</button>
    <button @click="toOrderForm">Cделать заказ</button>
  </div>
  <Diagramm />
  <div class="logout">
    <h1>Выйти из аккаунта</h1>
    <button>Выйти</button>
  </div>
</template>

<script>
import Diagramm from "@/components/Diagramm.vue";

export default {
  name: "user",
  components: {
    Diagramm,
  },
  data() {
    return {
      isManager: true,
    };
  },
  methods: {
    toOrderForm() {
      this.$router.push("/order");
    },
  },
};
</script>

import api from "@/api/axios"; export default { data() { return { userInfo:
null, error: "" }; }, async mounted() { try { const res = await
api.get("/user/protected"); this.userInfo = res.data.user; } catch (err) { if
(err.response && err.response.status === 401) {
localStorage.removeItem("jwt_token"); this.$router.push("/login"); } else {
this.error = "Ошибка получения данных пользователя"; } } } }

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
  display: flex;
  align-items: center;
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 80%;
  margin: 2rem auto;
  gap: 2rem;
}
.logout button {
  margin: 0 0;
}
.admin-button {
  background: rgb(246, 137, 38);
}
</style>
