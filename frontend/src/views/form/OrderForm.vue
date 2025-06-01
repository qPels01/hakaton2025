<template>
  <form @submit.prevent="submitForm">
    <h1>Заявка на создание проекта</h1>

    <label>Выберите тип проекта </label>
    <select v-model="selected1" required>
      <option v-for="item in dropdownProjectType" :key="item" :value="item">{{ item }}</option>
    </select>

    <label>Опишите, что должен уметь ваш проект</label>
    <textarea v-model="projectDescription"></textarea>

    <h1>Технологический стек</h1>

    <label>Выберите backend</label>
    <select v-model="selected2" required>
      <option v-for="item in dropdawnBackend" :key="item" :value="item">{{ item }}</option>
    </select>
    <label>Выберите базу данных</label>
    <select v-model="selected3" required>
      <option v-for="item in dropdawnDB" :key="item" :value="item">{{ item }}</option>
    </select>
    <label>Выберите frontend</label>
    <select v-model="selected4" required>
      <option v-for="item in dropdawnFrontEnd" :key="item" :value="item">{{ item }}</option>
    </select>

    <div id="checkbox">
      <input type="checkbox" v-model="chooseForMe" />
      <p id="checkbox-font">Я не знаю. Выберите всё за меня</p>
    </div>

    <div class="double-label">
      <h1>Когда вам нужен готовый проект?</h1>
      <p>(можете написать дату или промежуток времени)</p>
    </div>
    <input type="text" v-model="deadline" />

    <div class="double-label">
      <h1>Если есть что-то, что важно для вашего проекта, опишите здесь</h1>
      <p>(например, интеграция с платежной системой)</p>
    </div>
    <input type="text" v-model="importantDetails" />

    <div class="double-label">
      <h1>Укажите контактные данные</h1>
      <p>(если не указано, связь будет осуществляться по почте)</p>
    </div>
    <input type="text" v-model="contactInfo" />

    <button type="submit">Рассчитать</button>
  </form>
</template>

<script>
import api from "@/api/axios";
export default {
  name: "order",
  data() {
    return {
      dropdownProjectType: [
        "Сайт",
        "Одностраничный сайт (лендинг)",
        "Мобильное приложение",
        "Интернет-магазин",
        "Внутренний корпоративный портал",
        "Панель администратора",
        "Искусственный интеллект ",
        "API (сервис для взаимодействия)",
        "Доработка  существующего продукта",
        "Верстка",
        "Чат-бот",
        "Парсер",
        "Игра",
      ],
      dropdawnBackend: [
        "Php (рекомендуется)",
        "Python",
        "Node.js",
        "Java",
        "Go",
        "Ruby",
        "Kotlin",
        "Rust",
        "C#",
        "Без бекенда",
      ],
      dropdawnDB: ["SQL", "Firebase", "MongoDB", "Redis", "Без базы данных"],
      dropdawnFrontEnd: [
        "Html + css + javaScript",
        "Vue",
        "React",
        "Swift",
        "Java",
        "Kotlin",
        "Flatter",
      ],

      selected1: "",
      selected2: "",
      selected3: "",
      selected4: "",
      projectDescription: "",
      chooseForMe: false,
      deadline: "",
      importantDetails: "",
      contactInfo: "",
    };
  },
  methods: {
    async submitForm(evt) {
      // evt.preventDefault(); // НЕ нужно, если стоит @submit.prevent в шаблоне

      const data = {
        title: this.selected1,
        projectType: this.selected1,
        projectDescription: this.projectDescription,
        techStack: {
          backend: this.selected2,
          database: this.selected3,
          frontend: this.selected4,
          chooseForMe: this.chooseForMe,
        },
        deadline: this.deadline,
        importantDetails: this.importantDetails,
        contactInfo: this.contactInfo,
      };

      // Выводим собранные значения в консоль
      console.log(JSON.stringify(data, null, 2));

      // Можно отправлять запрос:
      try {
      console.log("Отправка заявки... ожидание..");
        const response = await api.post("/process", data);
        console.log(response.data);
      } catch (e) {
        console.error(e);
      }
    },
  },
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  margin: 2rem auto;
  width: 50%;
  background: #42464e;
  text-align: left;
  padding: 2rem;
  border-radius: 1.25rem;
  gap: 1.25rem;
}
h1 {
  text-align: center;
}
.double-label {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.double-label h1,
.double-label p {
  margin: 0;
  font-weight: normal;
  text-align: left;
  font-size: 1.25rem;
}
label {
  color: #ffffff;
  font-size: 1.125rem;
}
input {
  background: #42464e;
  border: 0.1rem solid #bbbbbb;
  border-radius: 1.25rem;
  height: 2rem;
  color: white;
  font-size: 1.2rem;
  padding: 0.25rem 1.25rem;
}
select {
  background: #42464e;
  border: 0.1rem solid #bbbbbb;
  border-radius: 2rem;
  height: 2.2rem;
  color: white;
  font-size: 1.2rem;
  padding: 0 12px;
}
#checkbox {
  display: flex;
  align-items: center;
  color: #ffffff;
  gap: 0.3rem;
  font-size: 1.25rem;
}
#checkbox-font {
  color: #ffffff;
}
#checkbox input {
  width: 1.25rem;
}
textarea {
  background: #42464e;
  border: 0.1rem solid #bbbbbb;
  border-radius: 0.75rem;
  height: 6.25rem;
  color: white;
  font-size: 1.2rem;
  padding: 0.5rem 0.75rem;
}
</style>
