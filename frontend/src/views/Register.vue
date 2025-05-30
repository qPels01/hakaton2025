<template>
  <form>
    <h1>Регистрация</h1>
    <label>название компании</label>
    <input type="text" required />
    <label>Email</label>
    <input type="text" required />
    <label>Пароль</label>
    <input type="password" required />
    <label>Подтвердить пароль</label>
    <input type="password" required />

    <button>Зарегистрироваться</button>
  </form>
</template>

<script>
export default {
  name: "register",
  data() {
    return {};
  },
};
</script>

<style></style>
