<script>
import api from "@/api/axios";

export default {
  name: "register",
  data() {
    return {
      username: "",
      email: "",
      company_name: "",
      password: "",
      password2: "",
      error: "",
      message: "",
    };
  },
  methods: {
    async onSubmit(e) {
      e.preventDefault();
      if (this.password !== this.password2) {
        this.error = "Пароли не совпадают";
        return;
      }
      this.error = "";
      try {
        await api.post("/auth/register", {
          username: this.username,
          email: this.email,
          company_name: this.company_name,
          password: this.password,
        });
        this.message = "Успешно! Теперь войдите.";
      } catch (err) {
        this.error =
          err.response?.data?.message ||
          "Ошибка регистрации или соединения с сервером";
      }
    },
  },
};
</script>
<template>
  <div class="formBox">
    <form @submit="onSubmit">
      <!-- поля ввода, как раньше -->
      <div class="field">
        <label>Имя пользователя</label>
        <input type="text" required v-model="username" />
      </div>
      <div class="field">
        <label>Email</label>
        <input type="text" required v-model="email" />
      </div>
      <div class="field">
        <label>Название организации</label>
        <input type="text" v-model="company_name" />
      </div>
      <div class="field">
        <label>Пароль</label>
        <input type="password" required v-model="password" />
      </div>
      <div class="field">
        <label>Подтвердить пароль</label>
        <input type="password" required v-model="password2" />
      </div>
      <div v-if="error" style="color:red;">{{ error }}</div>
      <div v-if="message" style="color:green;">{{ message }}</div>
      <button type="submit">Зарегистрироваться</button>
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
  font-size: 20px;
  transition: transform 0.5s ease;
  padding: 20px;
  margin-top: 10px;
}
button:hover {
  background: #497bdf;
  cursor: pointer;
  transform: scale(1.1);
}
</style>
