<template>
  <div class="main-container">
    <div class="nav-btn-container">
      <button @click="toUser">В профиль</button>
    </div>
    <div class="head-component">
      <h1>Список заявок</h1>
    </div>
    <ul class="card-list">
      <li v-for="item in teams" :key="item.id" class="card">
        <span>{{ item.company }}</span>
        <span>{{ item.order }}</span>
        <span>{{ item.date }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  methods: {
    toUser() {
      this.$router.push("/user");
    },
  },
  name: "teamLOg",
  data() {
    return {
      teams: [
        {
          company: "x5group",
          order: "Сайт",
          date: "02.06.25",
        },
        {
          company: "Сбер",
          order: "Искусственный интеллект",
          date: "01.04.25",
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
.nav-btn-container {
  width: 100%;
  display: flex;
  justify-content: flex-end;
  padding-right: 3rem;
  margin-bottom: 0;
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
button {
  padding: 1rem;
  margin: 0;
  width: 10rem;
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
