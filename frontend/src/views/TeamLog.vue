<template>
  <div class="main-container">
    <div class="head-component">
      <h1>Список разработчиков</h1>
    </div>
    <ul class="card-list">
      <li v-for="item in teams" :key="item.id" class="card">
        <span>Имя: {{ item.name }}</span>
        <span>{{ item.role }}</span>
        <span>Стек: {{ item.stack }}</span>
        <span>Команда 1</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "teamLOg",
  data() {
    return {
      teams: [
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Анна Иванова",
          email: "anna.ivanova@example.com",
          role: "frontend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Сергей Петров",
          email: "sergey.petrov@example.com",
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Мария Кузнецова",
          email: "maria.kuznetsova@example.com",
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Дмитрий Сидоров",
          email: "dmitry.sidorov@example.com",
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Елена Павлова",
          email: "elena.pavlova@example.com",
          role: "backend",
        },
      ],
    };
  },
};
</script>

<style scoped>
.teamer-btn {
  max-width: 10rem;
  padding: 0.5rem;
  margin: 0;
}
li {
  list-style: none;
}
.main-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin: 3rem auto;
  gap: 3rem;
}
.head-component {
  width: 50%;
  text-align: center;
  margin: 2rem auto;
  border-bottom: 0.1rem solid #969595;
}
.card-list {
  display: flex;
  flex-direction: column;
  max-width: 70rem;
  width: 100%;
  gap: 3rem;
  margin: 0;
  padding: 0;
}
.card {
  display: flex;
  justify-content: space-between;
  border-bottom: 0.1rem solid #969595;
  align-items: center;
  padding: 2rem;
  gap: 5rem;
}
span {
  color: white;
  font-size: 1.25rem;
}
</style>
