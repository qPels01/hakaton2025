<template>
  <div class="user-info" v-if="userInfo">
    <h1>Имя пользователя: {{ userInfo.username }}</h1>
  </div>
  <div class="admin-panel" v-if="userInfo && isManager">
    <button class="admin-button">Посмотреть заявки</button>
    <button @click="toDevList" class="admin-button">
      Список разработчиков
    </button>
  </div>
  <button @click="toOrderForm" v-if="userInfo && !isManager" class="admin-button">
    Cделать заказ
  </button>
  <Diagramm v-if="userInfo" />
  <div class="logout">
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
  },  computed: {
    isManager() {
      return this.userInfo && this.userInfo.role !== 'manager';
    }
  },
  methods: {
    toOrderForm() {
      this.$router.push("/order");
    },
    toDevList() {
      this.$router.push("/devlist");
    },    logout() {
      localStorage.removeItem('jwt_token');
      window.dispatchEvent(new Event('storage'));
      this.$router.push('/login');
    }
  },async mounted() {
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
