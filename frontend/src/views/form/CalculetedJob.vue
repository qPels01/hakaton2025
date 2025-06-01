<template>
  <div class="main-container">
    <div class="project-container">
      <h1 class="page-title" id="title">Рассчитанные трудозатраты</h1>

      <div id="times">
        <ul class="times-container">
          <li>
            <h1>Время на разработку</h1>
            <p>7 дней</p>
          </li>
          <li>
            <h1>Часов разработки</h1>
            <p>57</p>
          </li>
        </ul>
      </div>

      <div class="site-description">
        <h1 id="title">Подобранная команда</h1>
        <ul class="card-list">
          <li class="card">
            <span>Имя: </span>
            <span></span>
            <span>Стек:</span>
            <span>Команда 1</span>
            <!-- <button class="teamer-btn">подробнее</button> -->
          </li>
        </ul>
        <!-- <button>Принять</button> -->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "calcJob",
  data() {
    return {};
  },
};
</script>

<style scoped>
.main-container {
  display: flex;
  justify-content: center;
  margin: 0;
  padding: 0;
}
.project-container {
  display: flex;
  flex-direction: column;
  width: 50%;
  background-color: #42464e;
  border-radius: 2rem;
  padding: 3rem;
  margin: 3rem;
  gap: 2h1rem;
}
.page-title {
  border-bottom: 0.1rem solid #969595;
  padding: 1.5rem;
}
#site-title {
  text-align: center;
}
li {
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
h1 {
  font-size: 1.25rem;
}
#title {
  font-size: 1.5rem;
  text-align: center;
  border-bottom: 0.1rem solid #969595;
  padding: 1.5rem;
}
ul {
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>
