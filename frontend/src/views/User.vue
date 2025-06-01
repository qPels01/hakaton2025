<template>
  <div class="user-info">
    <h1>Имя пользователя: Иван Иванов Иванович</h1>
  </div>
  <div class="admin-panel">
    <button class="admin-button" v-if="isManager">Посмотреть заявки</button>
    <button @click="toDevList" class="admin-button" v-if="isManager">
      Список разработчиков
    </button>
    <button @click="toOrderForm">Cделать заказ</button>
  </div>
  <Diagramm />
  <div class="logout">
    <button>Выйти</button>
  </div>
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
    toDevList() {
      this.$router.push("/devlist");
    },
  },
};
</script>

<style scoped>
.user-info {
  display: block;
  background: #42464e;
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 80%;
  margin: 2rem auto;
}
.admin-panel {
  display: flex;
  align-items: center;
  background: #42464e;
  border-radius: 1.5rem;
  padding: 2rem;
  width: 100%;
  max-width: 80%;
  margin: 2rem auto;
  gap: 2rem;
}
.logout {
  padding: 2rem;
  margin: 2rem auto;
}
.admin-button {
  background: rgb(246, 137, 38);
}
.admin-button:hover {
  background: rgb(200, 112, 29);
}
</style>
