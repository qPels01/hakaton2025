<template>
  <div class="main-container">
    <div class="head-component">
      <h1>Список разработчиков</h1>
    </div>
    <select v-model="filterTeam">
      <option :value="null">Все команды</option>
      <option
        v-for="teamId in uniqueTeamIds"
        :key="teamId"
        :value="teamId"
      >
        Команда {{ teamId }}
      </option>
    </select>
    <ul class="card-list">
      <li v-for="dev in filteredTeams" :key="dev.id" class="card">
        <span>Имя: {{ dev.name }}</span>
        <span>Роль: {{ dev.role }}</span>
        <span>Стек: {{ dev.skills ? dev.skills.join(', ') : '' }}</span>
        <span>Уровень: {{ dev.level }}</span>
        <span>Ставка: {{ dev.hourly_rate_rub || '-' }}</span>
        <span>
          Команда {{ dev.team ? dev.team.id : '—' }}
        </span>
      </li>
    </ul>
    <div v-if="error" style="color:red">{{ error }}</div>
  </div>
</template>

<script>
import api from "@/api/axios";

export default {
  name: "devList",
  data() {
    return {
      filterTeam: null,
      devs: [],
      error: null,
    };
  },
  computed: {
    uniqueTeamIds() {
      // Собираем уникальные team.id для фильтра
      const ids = this.devs
        .map(dev => dev.team?.id)
        .filter(id => id != null);
      return [...new Set(ids)];
    },
    filteredTeams() {
      if (!this.devs.length) return [];
      return this.filterTeam
        ? this.devs.filter(dev => dev.team && dev.team.id == this.filterTeam)
        : this.devs;
    },
  },
  async mounted() {
    try {
      const res = await api.get("/developers");
      this.devs = res.data;
    } catch (e) {
      this.error = "Ошибка загрузки разработчиков";
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
