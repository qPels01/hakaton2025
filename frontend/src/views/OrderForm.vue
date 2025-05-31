<template>
  <form @submit.prevent="onSubmit">
    <h1>Заявка на создание проекта</h1>
    <label>Название проекта</label>
    <input v-model="title" type="text" required />

    <label>Выберите тип проекта</label>
    <select v-model="projectType" required>
      <option v-for="item in dropdownProjectType" :key="item" :value="item">{{ item }}</option>
    </select>
    <label>Опишите, что должен уметь ваш проект</label>
    <textarea v-model="projectDescription"></textarea>

    <h1>Технологический стек</h1>

    <label>Выберите backend</label>
    <select v-model="backend" required>
      <option v-for="item in dropdawnBackend" :key="item" :value="item">{{ item }}</option>
    </select>
    <label>Выберите базу данных</label>
    <select v-model="database" required>
      <option v-for="item in dropdawnDB" :key="item" :value="item">{{ item }}</option>
    </select>
    <label>Выберите frontend</label>
    <select v-model="frontend" required>
      <option v-for="item in dropdawnFrontEnd" :key="item" :value="item">{{ item }}</option>
    </select>

    <div id="checkbox">
      <input type="checkbox" v-model="autoStack" id="autoStack" />
      <p>Я не знаю. Выберите всё за меня</p>
    </div>

    <div class="double-label">
      <h1>Когда вам нужен готовый проект?</h1>
      <p>(можете написать дату или промежуток времени)</p>
    </div>
    <input v-model="deadline" type="text" />

    <div class="double-label">
      <h1>Если есть что-то, что важно для вашего проекта, опишите здесь</h1>
      <p>(например, интеграция с платежной системой)</p>
    </div>
    <input v-model="important" type="text" />

    <div class="double-label">
      <h1>Укажите контактные данные</h1>
      <p>(если не указано, связь будет осуществляться по почте)</p>
    </div>
    <input v-model="contact" type="text" />

    <button>Рассчитать</button>
        <div v-if="submitStatus" style="color:green">{{ submitStatus }}</div>
    <div v-if="submitError" style="color:red">{{ submitError }}</div>
  </form>
</template>
<script>
import { jwtDecode } from "jwt-decode";
import projectApi from "@/api/project_axios.js";

export default {
  name: "OrderForm",
  data() {
    return {
      title: "",

      projectType: "...",
      projectDescription: "",
      backend: "...",
      database: "...",
      frontend: "...",
      autoStack: false,
      deadline: "",
      important: "",
      contact: "",

      dropdownProjectType: [
        "Сайт", "Одностраничный сайт (лендинг)", "Мобильное приложение",
        "Интернет-магазин", "Внутренний корпоративный портал",
        "Панель администратора", "Искусственный интеллект ",
        "API (сервис для взаимодействия)", "Доработка  существующего продукта",
        "Верстка", "Чат-бот", "Парсер", "Игра",
      ],
      dropdawnBackend: [
        "...", "Php", "Python", "Node.js", "Java", "Go",
        "Ruby", "Kotlin", "Rust", "C#", "Без бекенда",
      ],
      dropdawnDB: ["...", "SQL", "Firebase", "MongoDB", "Redis", "Без базы данных"],
      dropdawnFrontEnd: [
        "...", "Html + css + javaScript", "Vue", "React",
        "Swift", "Java", "Kotlin", "FlatteR",
      ],
      
      submitStatus: "",
      submitError: ""
    };
  },
  methods: {
    async onSubmit() {
      const token = localStorage.getItem("jwt_token");
      let username = "", email = "", client_company = "",client_phone ="";
      if (token) {
        try {
          const decoded = jwtDecode(token);
          username = decoded.username;
          email = decoded.email;
          client_company = decoded.company_name;
        } catch {
          username = "";
          email = "";
          client_company = "";
        }
      }
      const description = [
        `Тип проекта: ${this.projectType}`,
        this.projectDescription ? `Что должен уметь проект: ${this.projectDescription}` : "",
        this.backend != "..." ? `Бэкенд: ${this.backend}` : "",
        this.database != "..."  ? `База данных: ${this.database}` : "",
        this.frontend != "..."  ? `Фронтенд: ${this.frontend}` : "",
        this.autoStack ? "Выбрать всё за меня: да" : "",
        this.deadline ? `Дедлайн: ${this.deadline}` : "",
        this.important ? `Важное: ${this.important}` : "",
      ].filter(Boolean).join(", ");

      const title = this.title;
      client_phone = this.contact;

      const result = {
        title,
        description,
        client_name: username,
        client_email: email,
        client_company,
        client_phone
      };

      console.log("Order submit:", result);

      this.submitStatus = "";
      this.submitError = "";
      try {
        await projectApi.post("/projects", result);
        this.submitStatus = "Заявка отправлена успешно!";
      } catch (err) {
        this.submitError = err.response?.data?.message || "Ошибка отправки";
        console.error("Ошибка отправки в projectApi", err);
      }
    }
  }
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  margin: 30px auto;
  width: 50%;
  background: #42464e;
  text-align: left;
  padding: 30px;
  border-radius: 20px;
  gap: 20px;
}
h1 {
  color: white;
  font-weight: bold;
  text-align: center;
  font-size: 30px;
}
.double-label h1 {
  color: white;
  font-weight: normal;
  text-align: left;
  font-size: 20px;
}
.double-label p {
  color: #ffffff;
  font-size: 15px;
}
label {
  color: #ffffff;
  font-size: 20px;
}
input {
  background: #42464e;
  border: 1.5px solid #bbbbbb;
  border-radius: 12px;
  height: 36px;
  color: white;
  font-size: 1.2rem;
  padding: 4px 12px;
}
select {
  background: #42464e;
  border: 1.5px solid #bbbbbb;
  border-radius: 12px;
  height: 36px;
  color: white;
  font-size: 1.2rem;
  padding: 0 12px;
}
#checkbox {
  display: flex;
  align-items: center;
  color: #ffffff;
  gap: 5px;
  font-size: 20px;
}
#checkbox input {
  width: 20px;
}
button {
  align-self: center;
  text-align: center;
  width: 50%;
  height: 15%;
  background: #548dff;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 25px;
  transition: transform 0.5s ease;
  padding: 20px;
  margin: 2.25rem;
}
button:hover {
  background: #497bdf;
  cursor: pointer;
  transform: scale(1.1);
}
option {
  color: #bbbbbb;
}
textarea {
  background: #42464e;
  border: 1.5px solid #bbbbbb;
  border-radius: 12px;
  height: 6.25rem;
  color: white;
  font-size: 1.2rem;
  padding: 8px 12px;
}
</style>
