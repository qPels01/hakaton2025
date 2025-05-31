<script>
import api from "@/api/axios";

export default {
  name: "login",
  data() {
    return {
      username: "",
      password: "",
      error: "",
    };
  },
  methods: {
    async onSubmit(e) {
      e.preventDefault();
      this.error = "";
      try {
        const res = await api.post("/auth/login", {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("jwt_token", res.data.token);
        this.$router.push("/user");
      } catch (err) {
        this.error =
          err.response?.data?.message ||
          "Ошибка входа или соединения с сервером";
      }
    },
    goToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>

<template>
  <div class="formBox">
    <form @submit="onSubmit">
      <h1>Вход</h1>
      <div class="field">
        <label>Имя пользователя</label>
        <input type="text" required v-model="username" />
      </div>
      <div class="field">
        <label>Пароль</label>
        <input type="password" required v-model="password" />
      </div>

      <div v-if="error" style="color: red">{{ error }}</div>
      <button type="submit">Войти</button>
      <button @click="goToRegister" type="button">Зарегистрироваться</button>
    </form>
  </div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 20rem;
  margin: 2rem auto;
  background: #42464e;
  text-align: left;
  padding: 2rem;
  border-radius: 1.5rem;
  gap: 1.75rem;
}
h1 {
  text-align: center;
  font-weight: bold;
}
input {
  background: #42464e;
  border: 0.1rem solid #bbbbbb;
  border-radius: 0.8rem;
  height: 2rem;
  color: white;
  font-size: 1.2rem;
  padding: 0.2rem 0.5rem;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
</style>
