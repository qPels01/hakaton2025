<template>
  <form>
    <h1>Заявка на создание проекта</h1>

    <label>Выберите тип проекта </label>
    <select v-model="selected1" required>
      <option v-for="item in dropdownProjectType" :key="item" :value="item">
        {{ item }}
      </option>
    </select>
    <label>Опишите, что должен уметь ваш проект</label>
    <textarea></textarea>

    <h1>Технологический стек</h1>

    <label>Выберите backend</label>
    <select v-model="selected2" required>
      <option v-for="item in dropdawnBackend" :key="item" :value="item">
        {{ item }}
      </option>
    </select>
    <label>Выберите базу данных</label>
    <select v-model="selected3" required>
      <option v-for="item in dropdawnDB" :key="item.value" :value="item.value">
        {{ item }}
      </option>
    </select>
    <label>Выберите frontend</label>
    <select v-model="selected4" required>
      <option v-for="item in dropdawnFrontEnd" :key="item" :value="item">
        {{ item }}
      </option>
    </select>

    <div id="checkbox">
      <input type="checkbox" />
      <p>Я не знаю. Выберите всё за меня</p>
    </div>

    <div class="double-label">
      <h1>Когда вам нужен готовый проект?</h1>
      <p>(можете написать дату или промежуток времени)</p>
    </div>
    <input type="text" />
    <div class="double-label">
      <h1>Если есть что-то, что важно для вашего проекта, опишите здесь</h1>
      <p>(например, интеграция с платежной системой)</p>
    </div>
    <input type="text" />
    <div class="double-label">
      <h1>Укажите контактные данные</h1>
      <p>(если не указано, связь будет осуществляться по почте)</p>
    </div>
    <input type="text" />

    <button>Рассчитать</button>
  </form>
</template>

<script>
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

      selected1: "a",
      selected2: "a",
      selected3: "a",
      selected4: "a",
    };
  },
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
