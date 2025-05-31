<template>
  <div class="user-data-block">
    <div class="user-info">
      <h1>Имя пользователя: Иван Иванов Иванович</h1>
      <h1>Email: example@mail.com</h1>
    </div>
    <div class="admin-panel" v-if="isManager">
      <button>Посмотреть заявки</button>
      <button>Список команд</button>
      <button>Список разработчиков</button>
    </div>
    <h1>Данные о заказах</h1>
    <Diagramm />
  </div>

  <button @click="toOrderForm">Cделать заказ</button>
  <button>Выйти</button>
</template>

<script>
import Diagramm from "@/components/Diagramm.vue";

export default {
  name: "user",
  components: {
    Diagramm,
  },
  data() {
    return {
      isManager: true,
    };
  },
  methods: {
    toOrderForm() {
      this.$router.push("/order");
    },
  },
};
</script>

<style scoped>
.user-info {
  background: #42464e;
  border-radius: 20px;
  padding: 20px;
  color: white;
  margin-bottom: 20px;
  width: 100%;
}
.user-data-block {
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  width: 80%;
}
h1 {
  color: white;
  text-align: center;
}
button {
  display: block;
  margin: 40px auto;
  width: 28%;
  height: 5.625rem;
  background: #548dff;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 25px;
  transition: transform 0.5s ease;
  padding: 20px;
  margin-top: 6.25rem;
}
button:hover {
  background: #497bdf;
  cursor: pointer;
  transform: scale(1.1);
}
.admin-panel {
  display: flex;
  justify-content: flex-start;
  width: 100%;
}
.admin-panel button {
  width: max-content;
  min-width: 120px;
  height: 3.5rem;
  margin: 0 20px 0 0; /* или просто margin: 0 20px 0 0; */
  padding: 10px 25px;
}
.admin-panel button:last-child {
  margin-right: 0;
}
</style>
