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

<script>
import Diagramm from "@/components/Diagramm.vue";
import api from "@/api/axios";

export default {
  name: "user",
  components: { Diagramm },
  data() {
    return {
      userInfo: null,
      error: "",
      isManager: true
    };
  },
  computed: {
    isManager() {
      return this.userInfo && this.userInfo.role === 'manager';
    }
  },
  methods: {
    toOrderForm() {
      this.$router.push("/order");
    },
    logout() {
      localStorage.removeItem('jwt_token');
      window.dispatchEvent(new Event('storage'));
      this.$router.push('/login');
    }
  },
  async mounted() {
    try {
      const res = await api.get("/user/protected"); // предполагается, что этот роут возвращает { user: { username, email, ... } }
      this.userInfo = res.data.user;
    } catch (err) {
      if (err.response && err.response.status === 401) {
        localStorage.removeItem("jwt_token");
        this.$router.push("/login");
      } else {
        this.error = "Ошибка получения данных пользователя";
      }
    }
  }
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
