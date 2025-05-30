<template>
  <header>
    <div class="logo">
      <h1>Байтики</h1>
      <img id="icon-logo" src="../assets/header/Blogo.svg" />
    </div>
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
  border-bottom: 1px solid #969595;
  height: 5rem;
  width: 100%;
  padding: 30px 90px;
}
#icon-logo {
  height: 2rem;
  width: 2rem;
}
.logo {
  display: flex;
  justify-content: center;
  color: white;
  gap: 0.8rem;
}
h1 {
  font-weight: bold;
  font-size: 30px;
}
</style>
