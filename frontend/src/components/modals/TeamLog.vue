<template>
  <div @click="closeModal" class="backdrop">
    <div class>
      <h1>dasfsafasf</h1>
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
  width: 80%;
  height: max-content;
  padding: 60px;
  background: #42464e;
}
</style>
