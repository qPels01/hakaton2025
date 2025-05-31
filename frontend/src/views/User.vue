<template>
  <div class="user-data-block">
    <div class="user-info" v-if="userInfo">
      <h1>Имя пользователя: {{ userInfo.username }}</h1>
      <h1>Email: {{ userInfo.email }}</h1>
    </div>
    <div v-else style="color: red;">{{ error }}</div>

    <div class="admin-panel" v-if="userInfo && isManager">
      <button>Посмотреть заявки</button>
      <button>Список команд</button>
      <button>Список разработчиков</button>
    </div>
    <Diagramm v-if="userInfo" />
  </div>

  <button @click="toOrderForm" v-if="userInfo">Сделать заказ</button>
  <button @click="logout" v-if="userInfo">Выйти</button>
</template>

<script>
import Diagramm from "@/components/Diagramm.vue";
import api from "@/api/axios";

export default {
  name: "User",
  components: { Diagramm },
  data() {
    return {
      userInfo: null,
      error: ""
    };
  },
  computed: {
    isManager() {
      // Типичная структура полей с ролью: user.role === 'manager'
      return this.userInfo && this.userInfo.role === 'manager';
    }
  },
  methods: {
    toOrderForm() {
      this.$router.push("/order");
    },
    logout() {
      // Удаляем токен и редиректим на /login
      localStorage.removeItem("jwt_token");
      this.$router.push("/login");
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
  background: #42464e;
  border-radius: 20px;
  padding: 20px;
  color: white;
  margin-bottom: 20px;
  width: 100%;
}
.user-data-block {
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  width: 80%;
}
h1 {
  color: white;
  text-align: center;
}
button {
  display: block;
  margin: 40px auto;
  width: 28%;
  height: 5.625rem;
  background: #548dff;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 25px;
  transition: transform 0.5s ease;
  padding: 20px;
  margin-top: 6.25rem;
}
button:hover {
  background: #497bdf;
  cursor: pointer;
  transform: scale(1.1);
}
.admin-panel {
  display: flex;
  justify-content: flex-start;
  width: 100%;
}
.admin-panel button {
  width: max-content;
  min-width: 120px;
  height: 3.5rem;
  margin: 0 20px 0 0; /* или просто margin: 0 20px 0 0; */
  padding: 10px 25px;
}
.admin-panel button:last-child {
  margin-right: 0;
}
</style>
