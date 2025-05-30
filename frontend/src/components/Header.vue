<template>
  <header>
    <div class="logo">
      <h1>Байтики</h1>
      <img src="../assets/header/Blogo.svg" alt="logo" />
    </div>
    <img src="../assets/header/профиль.svg" alt="user" />
  </header>
</template>

<script>
export default {
  name: "header",
};
</script>

<style>
header {
  display: flex;
  flex-direction: column;
  border-bottom: 1px solid #969595;
  height: 5rem;
  width: 100%;
  padding: 0 90px;
}
.logo img {
  height: 2rem;
  width: 2rem;
  display: block;
}
.logo {
  display: flex;
  align-items: baseline;
  color: white;
  gap: 0.8rem;
}
h1 {
  font-weight: bold;
  font-size: 30px;
}
</style>
