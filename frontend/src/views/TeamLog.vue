<template>
  <div class="main-container">
    <h1>Разработчики команды №{{ teamId }}</h1>
    <ul v-if="developers.length" class="card-list">
      <li v-for="dev in developers" :key="dev.id" class="card">
        <div><span class="label">Имя:</span> {{ dev.name }}</div>
        <div><span class="label">Роль:</span> {{ dev.role }}</div>
        <div><span class="label">Стек:</span> {{ dev.skills?.join(', ') }}</div>
        <div><span class="label">Уровень:</span> {{ dev.level }}</div>
        <div><span class="label">Ставка:</span> {{ dev.hourly_rate_rub }}</div>
      </li>
    </ul>
    <div v-else>
      Нет разработчиков для этой команды
    </div>
    <div v-if="error" style="color: red">{{ error }}</div>
  </div>
</template>

<script>
import api from '@/api/axios';

export default {
  name: 'TeamPage',
  data() {
    return {
      teamId: null,
      developers: [],
      error: null,
    };
  },
  async mounted() {
    this.teamId = Number(this.$route.params.id);
    try {
      const res = await api.get(`/teams/${this.teamId}`);
      this.developers = res.data.developers || [];
    } catch (e) {
      this.error = 'Ошибка загрузки';
    }
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
