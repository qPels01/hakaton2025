<template>
  <div class="main-container">
    <div class="project-container">
      <h1 id="title">Просмотр заявки</h1>
      <div class="container">
        <ul>
          <li>
            <h1>Заказчик</h1>
            <p>{{ client.name }}</p>
          </li>
          <li>
            <h1>Дата подачи заявки</h1>
            <p>{{ cleanCreated_at }}</p>
          </li>
          <li>
            <h1>Контактные данные</h1>
            <p>{{ query.contactInfo }}</p>
          </li>
        </ul>
      </div>

      <div class="container">
        <h1 id="title">{{ query.title }}</h1>
        <p class="side-container-desc">{{ query.projectDescription }}</p>
        <ul>
          <li>
            <h1 class="subtitle">Бекенд</h1>
            <p>{{ tasks.chosenStack.backend }}</p>
          </li>
          <li>
            <h1 class="subtitle">Фронтенд</h1>
            <p>{{ tasks.chosenStack.frontend }}</p>
          </li>
          <li>
            <h1 class="subtitle">База данных</h1>
            <p>{{ tasks.chosenStack.database }}</p>
          </li>
        </ul>

        <div class="deadline">
          <h1 class="subtitle">Дедлайн:</h1>
          <p>{{ query.deadline }}</p>
        </div>

        <div class="side-container">
          <h1 class="subtitle">Дополнительные пожелания:</h1>
          <p>{{ query.importantDetails }}</p>
        </div>
      </div>

      <div class="container">
        <h1 id="title">Рассчитанные трудозатраты</h1>
        <ul>
          <li>
            <h1 class="subtitle">Время на разработку</h1>
            <p>
              {{ tasks.total_estimated_time.toString() + " дней" }}
            </p>
          </li>
          <li>
            <h1 class="subtitle">Часов разработки</h1>
            <p>
              {{ tasks.total_estimated_time.toString() + " ч" }}
            </p>
          </li>
          <li>
            <h1 class="subtitle">Общая стоимость</h1>
            <p>{{ spending.total_cost.toLocaleString("ru-Ru") }} ₽</p>
          </li>
        </ul>
      </div>

      <div class="container">
        <h1 id="subtitle">
          Подобранная команда
          {{ "(Команда " + tasks.chosen_team_id.toString() + "):" }}
        </h1>
        <div
          class="dev-side-container"
          v-for="(dev, index) in developers"
          :key="index"
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
            <ul v-for="calc in spending.calculation" :key="calc.id">
              <li v-if="calc.dev_id == index">
                <p class="subtitle">Часов разработки</p>
                <p>{{ calc.hours }}</p>
              </li>
              <li v-if="calc.dev_id == index">
                <p class="subtitle">Стоимость работы</p>
                <p>{{ calc.cost }}</p>
              </li>
            </ul>
          </ul>
        </div>
      </div>

      <div class="container">
        <h1 id="subtitle">Задачи</h1>
        <li v-for="(task, index) in tasks.tasks">
          <ul>
            <li class="tasks-index">{{ index }}</li>
            <li class="tasks" v-for="rtask in task">
              <div class="side-container-tasks">
                <p class="label subtitle">{{ rtask.title }}</p>
                <p>{{ rtask.description }}</p>
                <p>
                  {{ "Рассчитанное время: " + rtask.estimated_hours + "ч" }}
                </p>
              </div>
            </li>
          </ul>
        </li>
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
  name: "projects",
  data() {
    return {
      client: {
        name: "x5group",
      },
      developers: {
        1: {
          name: "Иван Иванович",
          role: "frontend",
          level: "junior",
          skills: ["SQL", "php"],
          hourly_rate_rub: 10000,
        },
        2: {
          name: "Кузнец Кузнецов",
          role: "qa",
          level: "senior",
          skills: ["python"],
          hourly_rate_rub: 1000,
        },
      },
      query: {
        title: "Курсы английского EasyLearn",
        projectType: "Лендинг",
        projectDescription:
          "Современный сайт-визитка для школы английского языка с формой заявки и описанием преимуществ.",
        techStack: {
          backend: "-",
          database: "-",
          frontend: "html + css",
          chooseForMe: false,
        },
        deadline: "2 недели",
        importantDetails:
          "Необходимо сделать акцент на легкость восприятия и дружелюбный стиль. Форма обратной связи обязательна.",
        contactInfo: "easylearn.site@gmail.com",
      },

      tasks: {
        today: "2025-06-01T00:30:16.603Z",
        projectTitle: "Курсы английского EasyLearn",
        chosenStack: {
          backend: "-",
          frontend: "html + css",
          database: "-",
        },
        tasks: {
          backend: [],
          frontend: [
            {
              title: "Верстка лендинга EasyLearn",
              description:
                "Создать современный адаптивный лендинг для школы английского языка с акцентом на легкость восприятия, описание преимуществ и обязательной формой обратной связи.",
              estimated_hours: 18,
            },
          ],
          qa: [
            {
              title: "Тестирование лендинга",
              description:
                "Проверить корректность отображения на десктопе и мобильных, работу формы обратной связи, орфографию и доступность.",
              estimated_hours: 4,
            },
          ],
        },
        total_estimated_time: 22,
        estimated_finish_date: "2025-06-07",
        chosen_team_id: 1,
      },
      spending: {
        calculation: [
          {
            role: "frontend",
            hours: 18,
            hourly_rate: 2000,
            count: 1,
            cost: 36000,
            dev_id: 1,
          },
          {
            role: "qa",
            hours: 4,
            hourly_rate: 1250,
            count: 1,
            cost: 5000,
            dev_id: 2,
          },
        ],
        total_cost: 41000,
      },
    };
  },
  computed: {
    cleanCreated_at() {
      return getCleanDate(this.tasks.today);
    },
  },
  methods: {
    getStack(stack) {
      return stack.join(", ");
    },
  },
};

function getCleanDate(date) {
  let dateAndTime = date.split("T");
  return dateAndTime[0];
}
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
