<script>
import { RouterLink, RouterView } from "vue-router";
import Home from "@/views/Home.vue";
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";

export default {
    name: "app",
    components: { Header, Footer },
};
</script>

<template>
    <div id="app">
        <Header />

        <main>
            <RouterLink to="/"></RouterLink>
            <RouterView />
        </main>

        <Footer />
    </div>
</template>

<style>
html,
body,
#app {
    height: 100%;
    margin: 0;
    display: flex;
    flex-direction: column;
}
main {
    flex: 1 0 auto;
}
</style>
