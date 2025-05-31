<template>
  <div class="project-container">
    <h1 class="page-title">Просмотр заявки</h1>
    <ul>
      <li>
        <label class="subtitle" id="project">Заказчик</label>
        <label class="label">{{ client }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Почта заказчика</label>
        <label class="label">{{ client_email }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Дата подачи заявки</label>
        <label class="label">{{ date }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Контактные данные</label>
        <label class="label">{{ contacts }}</label>
      </li>
    </ul>

    <h1>{{ title }}</h1>
    <label> {{ description }} </label>
    <ul>
      <li>
        <label class="subtitle" id="project">Бекенд</label>
        <label class="label">{{ backend }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Фронтенд</label>
        <label class="label">{{ frontend }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">База данных</label>
        <label class="label">{{ db }}</label>
      </li>
    </ul>
    <div>
      <label class="subtitle">Дедлайн: </label>
      <label class="label">{{ deadline }}</label>
    </div>
    <label class="subtitle">Дополнительные пожелания:</label>
    <label class="label">{{ extras }}</label>
    <h1 class="page-title">Рассчитанные трудозатраты</h1>
    <ul>
      <li>
        <label class="subtitle" id="project">Время на разработку</label>
        <label class="label">{{ days.toString() + " дней" }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Часов разработки</label>
        <label class="label">{{ hours.toString() + " ч" }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Общая стоимость</label>
        <label class="label">{{ total_cost.toString() + "" }}</label>
      </li>
    </ul>
    <div>
      <label class="subtitle" id="project">Подобранная команда</label>
      <label class="label">{{ "(" + team + "):" }}</label>
    </div>
    <button id="accept">Подтвердить выбор ИИ</button>
    <button id="recalc">Перерасчитать</button>
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
      description: "Нам нужен сайт для подготовки юных кассиров. У учеников должен быть доступ в систему  через Яндекс Почту. Lms должна уметь выводить задания и выставлять за них баллы",
      backend: "не принципиально",
      frontend: "vue",
      db: "SQL",
      deadline: "5.07.25",
      extras: "Важно, чтобы во vue использовался TypeScript. Также нужна интеграция с платёжной системой для оплаты наших курсов",
      days: 7,
      hours: 120,
      total_cost: 96900,
      team: "Команда 1",
    };
  },
};
</script>

<style scoped>
  .project-container{
    width: 70%;
    background-color: #42464E;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    margin: 30px auto;
    padding: 0 90px 40px 90px;
    gap: 20px;
  }
  #accept{
    margin: 0;
  }
  ul{
    color: white;
    margin: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  #project{
    margin-right: 15px;
    margin-bottom: 32px;
  }
  #recalc{
    background: #889DC7;
    margin: 0;
  }
</style>