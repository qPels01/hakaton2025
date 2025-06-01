<template>
  <div class="main-container" v-if="query">
    <div class="project-container">
      <h1 id="title">Просмотр заявки</h1>
      <div class="container">
        <ul>
          <li>
            <h1>Заказчик</h1>
            <p>{{ customer.username || "Не указано" }}</p>
          </li>
          <li>
            <h1>Дата подачи заявки</h1>
            <p>{{ (project.today || '').split('T')[0] }}</p>
          </li>
        </ul>
      </div>

      <div class="container">
        <h1 id="title">{{ project.projectTitle }}</h1>
        <ul>
          <li>
            <h1 class="subtitle">Бекенд</h1>
            <p>{{ chosenStack.backend }}</p>
          </li>
          <li>
            <h1 class="subtitle">Фронтенд</h1>
            <p>{{ chosenStack.frontend }}</p>
          </li>
          <li>
            <h1 class="subtitle">База данных</h1>
            <p>{{ chosenStack.database }}</p>
          </li>
        </ul>
        <div class="deadline">
          <h1 class="subtitle">Дедлайн:</h1>
          <p>{{ project.estimated_finish_date }}</p>
        </div>
      </div>

      <div class="container">
        <h1 id="title">Рассчитанные трудозатраты</h1>
        <ul>
          <li>
            <h1 class="subtitle">Время на разработку</h1>
            <p>
              {{ project.total_estimated_time }} дней
            </p>
          </li>
          <li>
            <h1 class="subtitle">Общая стоимость</h1>
            <p>{{ totalCost.toLocaleString("ru-Ru") }} ₽</p>
          </li>
        </ul>
      </div>

      <div class="container">
        <h1 id="subtitle">
          Подобранная команда
          {{ "(Команда " + (project.chosen_team_id || "") + "):" }}
        </h1>
        <div
          class="dev-side-container"
          v-for="(dev, index) in developers"
          :key="dev.id"
        >
          <ul class="developers">
            <li>
              <div class="about">
                <h1 class="subtitle noMargin">{{ dev.name }}</h1>
                <p class="with-dot">{{ dev.role }}</p>
                <p class="with-dot">{{ dev.level }}</p>
                <p class="with-dot">{{ getStack(dev.skills) }}</p>
              </div>
            </li>
            <li>
              <p class="subtitle">Часов разработки</p>
              <p>{{ devCalculation(dev.role).hours || 0 }}</p>
            </li>
            <li>
              <p class="subtitle">Стоимость работы</p>
              <p>{{ devCalculation(dev.role).cost || 0 }}</p>
            </li>
          </ul>
        </div>
      </div>

      <div class="container">
        <h1 id="subtitle">Задачи</h1>
        <ul>
          <li v-for="(taskArr, roleIndex) in allTasksMerged()" :key="roleIndex">
            <ul>
              <li
                v-for="(rtask, idx) in taskArr"
                :key="idx"
                class="tasks"
                style="margin-bottom: 1rem;"
              >
                <div class="side-container-tasks">
                  <p class="label subtitle">{{ rtask.title }}</p>
                  <p>{{ rtask.description }}</p>
                  <p>
                    {{ "Рассчитанное время: " + rtask.estimated_hours + " ч" }}
                  </p>
                </div>
              </li>
            </ul>
          </li>
        </ul>
      </div>
      <div class="buttons">
        <button id="denied">Отклонить</button>
        <button>Принять</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "requisition",
  data() {
    return {
      query: null
    };
  },
  computed: {
    project() { return this.query?.project ?? {}; },
    customer() { return this.project.customer ?? {}; },
    chosenStack() { return this.project.chosenStack ?? {}; },
    tasks() { return this.project.tasks ?? {}; },
    spending() { return this.query?.spending ?? {}; },
    calculations() { return this.spending.calculation ?? []; },
    team() { return this.query?.team ?? {}; },
    developers() { return this.team.developers ?? []; },
    totalCost() { return this.spending.total_cost || 0; }
  },
  mounted() {
    const stored = localStorage.getItem("lastRequisition");
    if (stored) {
      try {
        this.query = JSON.parse(stored);
        console.log("Заявка из localStorage:", this.query);
      } catch (e) {
        console.error("Ошибка парсинга заявки", e);
      }
    }
  },
  methods: {
    getStack(skills) {
      return Array.isArray(skills) ? skills.join(', ') : '';
    },
    devCalculation(devRole) {
      return this.calculations.find(calc => calc.role === devRole) || {};
    },
    allTasksMerged() {
      return Object.values(this.tasks)
        .filter(el => Array.isArray(el))
        .map(tasksArr => tasksArr || []);
    }
  }
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
  padding: 0.5rem 2rem;
  margin: 3rem;
  gap: 2rem;
}
.req-id {
  text-align: right;
  margin-top: 3rem;
}
.container {
  background: #30343b;
  padding: 1.5rem;
  border-radius: 1rem;
}
.side-container {
  background: #282b30;
  padding: 1.5rem;
  border-radius: 1rem;
}
.dev-side-container {
  background: #282b30;
  padding: 1.5rem;
  border-radius: 1rem;
  margin: 2rem;
}
.side-container-tasks {
  background: #2b2f34;
  padding: 1.5rem;
  border-radius: 0.5rem;
}
.side-container-desc {
  background: #282b30;
  padding: 1.5rem;
  border-radius: 1rem;
  text-align: center;
}
#title {
  border-bottom: 0.1rem solid #969595;
  padding: 1.5rem;
  font-size: 1.5rem;
  text-align: center;
}
#subtitle {
  border-bottom: 0.1rem solid #969595;
  padding: 1.5rem;
  font-size: 1.5rem;
  text-align: left;
}
.deadline {
  display: flex;
  justify-content: space-between;
  margin: 2rem auto;
  align-items: center;
}
.deadline p {
  font-size: 1.2rem;
  letter-spacing: 0.1rem;
}
p.with-dot::before {
  content: "•";
  color: #fff;
  margin-right: 0.5em;
  font-size: 1em;
}
.tasks {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
}
.tasks-index {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #282b30;
  padding: 1rem;
  border-radius: 1rem;
  margin: 0.3rem;
  color: #ffff;
  font-size: 1.25rem;
  font-weight: bold;
}
.tasks-index h1 {
  margin: 0;
  text-align: center;
}
.buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}
p {
  color: white;
  font-size: 1.1rem;
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
ul {
  width: 100%;
  margin: 0;
  padding: 0;
}
#denied {
  background: rgb(236, 17, 17);
}
#denied:hover {
  background: rgb(202, 17, 17);
}
</style>
