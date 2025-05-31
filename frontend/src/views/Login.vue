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
      <div v-if="error" style="color: red;">{{ error }}</div>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>


<style scoped>
form {
  display: flex;
  flex-direction: column;
  min-width: 300px;
  max-width: 22%;
  margin: 30px auto;
  background: #42464e;
  text-align: left;
  padding: 30px;
  border-radius: 20px;
  gap: 25px;
}
h1 {
  text-align: center;
  color: #ffffff;
  font-size: 40px;
  font-weight: bold;
}
label {
  color: #979797;
  display: inline-block;
  font-size: 1rem;
  letter-spacing: 1px;
}
input {
  background: #42464e;
  border: 1.5px solid #bbbbbb;
  border-radius: 12px;
  height: 36px;
  color: white;
  font-size: 1.2rem;
  padding: 4px 12px;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
button {
  align-self: center;
  text-align: center;
  width: 75%;
  height: 15%;
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
</style>
