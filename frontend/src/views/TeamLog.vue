<template>
  <div class="log-component">
    <h1>Список разработчиков</h1>
  </div>
  <div class="teamer-container">
    <div class="teamer">
      <h1>Иванов Георгий Георгинович</h1>
      <p>backend</p>
      <p>python, SQLite</p>
      <button class="teamer-btn">подробнее</button>
    </div>
  </div>
</template>

<script>
export default {
  name: { teamLOg },
};
</script>

<style scoped>
.log-component {
  display: flex;
  justify-content: center;
  width: 100%;
}
.log-component h1 {
  padding: 2rem;
  border-bottom: 0.1rem solid #969595;
}
.teamer-container {
  display: flex;
  justify-content: center;
  width: 100%;
  gap: 3rem;
  margin-top: 3rem;
}
.teamer {
  display: flex;
  gap: 10rem;
  padding: 1rem;
  border-bottom: 0.1rem solid #969595;
}
.teamer-btn {
  width: auto;
  max-width: none;
  min-width: 9rem;
  padding: 0.8em 2.5em;
  font-size: 1rem;
  border-radius: 2em;
  padding: 0.5em 2em;
  font-size: 1rem;
  height: 2.5em;
  line-height: 1.2;
  align-self: center;
}
</style>
