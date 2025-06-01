<template>
  <div class="project-container">
    <h1 class="page-title">Просмотр заявки</h1>
    <ul>
      <li>
        <label class="subtitle" id="project">Заказчик</label>
        <label class="label">{{ client.name }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Дата подачи заявки</label>
        <label class="label">{{ cleanCreated_at }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Контактные данные</label>
        <label class="label">{{ query.contactInfo }}</label>
      </li>
    </ul>

    <h1>{{ query.title }}</h1>
    <label> {{ query.projectDescription }} </label>
    <ul>
      <li>
        <label class="subtitle" id="project">Бекенд</label>
        <label class="label">{{ tasks.chosenStack.backend }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Фронтенд</label>
        <label class="label">{{ tasks.chosenStack.frontend }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">База данных</label>
        <label class="label">{{ tasks.chosenStack.database }}</label>
      </li>
    </ul>
    <div>
      <label class="subtitle">Дедлайн: </label>
      <label class="label">{{ query.deadline }}</label>
    </div>
    <label class="subtitle">Дополнительные пожелания:</label>
    <label class="label">{{ query.importantDetails }}</label>
    <h1 class="page-title">Рассчитанные трудозатраты</h1>
    <ul>
      <li>
        <label class="subtitle" id="project">Время на разработку</label>
        <label class="label">{{ tasks.total_estimated_time.toString() + " дней" }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Часов разработки</label>
        <label class="label">{{ tasks.total_estimated_time.toString() + " ч" }}</label>
      </li>
      <li>
        <label class="subtitle" id="project">Общая стоимость</label>
        <label class="label">{{ spending.total_cost.toString() + "" }}</label>
      </li>
    </ul>
    <div>
      <h1 class="page-title subtitle" id="project">Подобранная команда {{  "(Команда " + tasks.chosen_team_id.toString() + "):" }}</h1>
    </div>
    <ul class="developers" v-for="(dev, index) in developers">
      <li>
        <div class="about">
          <label class="subtitle noMargin" id="project">{{ dev.name }}</label>
          <label class="label">{{ dev.role }}</label>
          <label class="label">{{ dev.level }}</label>
          <label class="label">{{ getStack(dev.skills) }}</label>
        </div>
      </li>
      <ul v-for="calc in spending.calculation">
        <li v-if="calc.dev_id == index">
          <label class="subtitle" id="project">Часов разработки</label>
             <label class="label">{{calc.hours}} </label>
        </li>
        <li v-if="calc.dev_id == index">
          <label class="subtitle" id="project">Стоимость работы</label>
             <label class="label">{{calc.cost}} </label>
        </li>
      </ul>
    </ul>
    <ul>
        
    </ul>
    <button id="accept">Подтвердить выбор ИИ</button>
    <button id="recalc">Перерасчитать</button>
  </div>
</template>

<script>
export default {
  name: "projects",
  data() {
    return {
        "client":{
            "name": "x5group",
        },
        "developers":{
          1:{
            name:"Иван Иванович",
            role:"frontend",
            level:"junior",
            skills: ["SQL", "php"],
            hourly_rate_rub: 10000
          },
          2:{
            name:"Кузнец Кузнецов",
            role:"qa",
            level:"senior",
            skills: ["python"],
            hourly_rate_rub: 1000
          }
        },
          "query":{
              "title": "Курсы английского EasyLearn",
              "projectType": "Лендинг",
              "projectDescription": "Современный сайт-визитка для школы английского языка с формой заявки и описанием преимуществ.",
              "techStack": {
                "backend": "-",
                "database": "-",
                "frontend": "html + css",
                "chooseForMe": false 
              },
            "deadline": "2 недели",
            "importantDetails": "Необходимо сделать акцент на легкость восприятия и дружелюбный стиль. Форма обратной связи обязательна.",
            "contactInfo": "easylearn.site@gmail.com"
          },

        "tasks": {
            "today": "2025-06-01T00:30:16.603Z",
            "projectTitle": "Курсы английского EasyLearn",
            "chosenStack": {
                "backend": "-",
                "frontend": "html + css",
                "database": "-"
            },
            "tasks": {
                "backend": [],
                "frontend": [
                    {
                        "title": "Верстка лендинга EasyLearn",
                        "description": "Создать современный адаптивный лендинг для школы английского языка с акцентом на легкость восприятия, описание преимуществ и обязательной формой обратной связи.",
                        "estimated_hours": 18
                    }
                ],
                "qa": [
                    {
                        "title": "Тестирование лендинга",
                        "description": "Проверить корректность отображения на десктопе и мобильных, работу формы обратной связи, орфографию и доступность.",
                        "estimated_hours": 4
                    }
                ]
            },
            "total_estimated_time": 22,
            "estimated_finish_date": "2025-06-07",
            "chosen_team_id": 1
        },
        "spending": {
            "calculation": [
                {
                    "role": "frontend",
                    "hours": 18,
                    "hourly_rate": 2000,
                    "count": 1,
                    "cost": 36000,
                    "dev_id": 1
                },
                {
                    "role": "qa",
                    "hours": 4,
                    "hourly_rate": 1250,
                    "count": 1,
                    "cost": 5000,
                    "dev_id": 2
                }
            ],
            "total_cost": 41000
        }
    };
  },
  computed: {
    cleanCreated_at(){
      return getCleanDate(this.tasks.today)
    },
  },
  methods: {
    getStack(stack){
      return stack.join(", ");
    }
  }
};

function getCleanDate(date){
  let dateAndTime = date.split('T');
  return dateAndTime[0];
}

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
  .about{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
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
  .subtitle{
      font-size: 24px;
  }
  .developers{
    border-bottom: 2px solid #ccc;
  margin-bottom: 0;
  }
</style>