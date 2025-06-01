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
        const res = await api.post("/auth/register", {
      username: this.username,
      email: this.email,
      company_name: this.company_name,
      password: this.password,
    });

    // Теперь можете обращаться к res.data.token
    if (res.data.token) {
      localStorage.setItem("jwt_token", res.data.token);
      window.dispatchEvent(new Event('storage'));
      this.$router.push("/user");
    } else {
      this.message = "Успешно! Теперь войдите.";
    }
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
      <h1>Регистрация</h1>

      <div class="field">
        <label>Имя пользователя</label>
        <input
          type="text"
          required
          v-model="username"
          name="username"
          autocomplete="username"
        />
      </div>
      <div class="field">
        <label>Email</label>
                <input
          type="email"
          required
          v-model="email"
          name="email"
          autocomplete="email"
        />
      </div>
      <div class="field">
        <label>Название организации</label>
        <input type="text" v-model="company_name" />
      </div>
      <div class="field">
        <label>Пароль</label>
                <input
          type="password"
          required
          v-model="password"
          name="password"
          autocomplete="current-password"
        />
      </div>
      <div class="field">
        <label>Подтвердить пароль</label>
               <input
          type="password"
          required
          v-model="password2"
          name="confirm_password"
          autocomplete="new-password"
        />
      </div>
      <div v-if="error" style="color: red">{{ error }}</div>
      <div v-if="message" style="color: green">{{ message }}</div>
      <button type="submit">Зарегистрироваться</button>
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
}
.field {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
</style>
