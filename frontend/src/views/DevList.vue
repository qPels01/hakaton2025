<template>
  <div class="main-container">
    <div class="head-component">
      <h1>Список разработчиков</h1>
    </div>
    <select v-model="filterTeam">
      <option :value="null">Все команды</option>
      <option v-for="n in [1, 2]" :key="n" :value="n">Команда {{ n }}</option>
    </select>
    <ul class="card-list">
      <li v-for="item in filteredTeams" :key="item.id" class="card">
        <span>Имя: {{ item.name }}</span>
        <span>{{ item.role }}</span>
        <span>Стек: {{ item.stack }}</span>
        <span>Команда {{ item.team }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "devList",
  data() {
    return {
      filterTeam: null,
      teams: [
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Анна Иванова",
          team: 1,
          role: "frontend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Сергей Петров",
          team: 1,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Мария Кузнецова",
          team: 1,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Дмитрий Сидоров",
          team: 1,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Елена Павлова",
          team: 1,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Елена Павлова",
          team: 1,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Елена Павлова",
          team: 2,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Елена Павлова",
          team: 2,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Елена Павлова",
          team: 2,
          role: "backend",
        },
        {
          stack: "React, Node.js, MongoDB Vue.js",
          name: "Елена Павлова",
          team: 2,
          role: "backend",
        },
      ],
    };
  },
  computed: {
    filteredTeams() {
      return this.filterTeam
        ? this.teams.filter((t) => t.team == this.filterTeam)
        : this.teams;
    },
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
select {
  width: 100%;
  max-width: 70rem;
  background: #42464e;
  border: 1.5px solid #bbbbbb;
  border-radius: 12px;
  height: 36px;
  color: white;
  font-size: 1.2rem;
  padding: 0 1rem;
}
</style>
