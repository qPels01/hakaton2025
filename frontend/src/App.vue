<script>
import { RouterLink, RouterView } from "vue-router";
import Home from "@/views/Home.vue";
import Header from "./components/Header.vue";

export default {
  name: "app",
  components: { Header },
};
</script>

<template>
  <Header />
  <RouterLink to="/"></RouterLink>
  <RouterView />
</template>

<style></style>
