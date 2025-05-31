<template>
  <div @click.self="closeModal" class="backdrop">
    <div class="modal">
      <div class="front">
        <h1>Список разработчиков</h1>
      </div>
      <div class="users">
        <h1>Иванов Георгий Георгинович</h1>
        <p>backend</p>
        <p>python, SQLite</p>
        <p></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "teamLog",
  methods: {
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>

<style scoped>
.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}
.modal {
  display: flex;
  margin: 15rem auto;
  width: 65%;
  height: max-content;
  padding: 60px;
  background: #42464e;
}
.front {
  margin: 2rem auto;
}
</style>
