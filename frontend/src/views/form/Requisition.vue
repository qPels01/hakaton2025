<template>
  <div class="main-container">
    <div class="project-container">
      <h1 class="page-title" id="title">Просмотр заявки</h1>

      <div id="customer">
        <ul class="customer-container">
          <li>
            <h1>Заказчик</h1>
            <p>{{ client }}</p>
          </li>
          <li>
            <h1>Почта заказчика</h1>
            <p>{{ client_email }}</p>
          </li>
          <li>
            <h1>Дата подачи заявки</h1>
            <p>{{ date }}</p>
          </li>
          <li>
            <h1>Контактные данные</h1>
            <p>{{ contacts }}</p>
          </li>
        </ul>
      </div>

      <div class="site-description">
        <h1 id="title">{{ title }}</h1>
        <p class="description-container">{{ description }}</p>
        <ul class="stack-container">
          <li>
            <h1>Бекенд</h1>
            <p>{{ backend }}</p>
          </li>
          <li>
            <h1>Фронтенд</h1>
            <p>{{ frontend }}</p>
          </li>
          <li>
            <h1>База данных</h1>
            <p>{{ db }}</p>
          </li>
        </ul>
        <div>
          <div class="deadline">
            <h1>Дедлайн:</h1>
            <p>{{ deadline }}</p>
          </div>
        </div>
        <h1>Дополнительные пожелания:</h1>
        <p class="dops-box">{{ extras }}</p>
      </div>

      <div class="spending">
        <h1 class="page-title" id="title">Рассчитанные трудозатраты</h1>
        <ul>
          <li>
            <h1>Время на разработку</h1>
            <p>{{ days.toString() + " дней" }}</p>
          </li>
          <li>
            <h1>Часов разработки</h1>
            <p>{{ hours.toString() + " ч" }}</p>
          </li>
          <li>
            <h1>Общая стоимость</h1>
            <p>{{ total_cost.toString() + "" }}</p>
          </li>
        </ul>
        <div class="teams">
          <h1>Подобранная команда</h1>
          <p>{{ "(" + team + ")" }}</p>
        </div>
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
      client: "x5group",
      client_email: "example@mail.ru",
      date: "31.05.2025",
      contacts: "не указано",
      title: "Сайт",
      description:
        "Нам нужен сайт для подготовки юных кассиров. У учеников должен быть доступ в систему  через Яндекс Почту. Lms должна уметь выводить задания и выставлять за них баллы",
      backend: "не принципиально",
      frontend: "vue",
      db: "SQL",
      deadline: "5.07.25",
      extras:
        "Важно, чтобы во vue использовался TypeScript. Также нужна интеграция с платёжной системой для оплаты наших курсов",
      days: 7,
      hours: 120,
      total_cost: 96900,
      team: "Команда 1",
    };
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
#customer {
  padding-bottom: 2rem;
  border-bottom: 0.1rem solid #969595;
}
.description-container {
  background: #282b30;
  padding: 1.5rem;
  border-radius: 1rem;
}
.deadline {
  border-top: 0.1rem solid #969595;
  padding-top: 2rem;
  display: flex;
  justify-content: space-between;
}
.stack-container {
  padding-bottom: 2rem;
}
.dops-box {
  background: #282b30;
  padding: 1.5rem;
  border-radius: 1rem;
}
.teams {
  display: flex;
  justify-content: space-between;
}
.buttons {
  display: flex;
  justify-content: center;
  margin: 3rem;
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
#title {
  font-size: 1.5rem;
  text-align: center;
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
