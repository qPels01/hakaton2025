<template>
  <div @click="closeModal" class="backdrop">
    <h1>dasfsafasf</h1>
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
  top: 0;
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  width: 100%;
  height: 100%;
}
.modal {
  width: 80%;
  height: max-content;
  padding: 60px;
  background: #42464e;
}
</style>
