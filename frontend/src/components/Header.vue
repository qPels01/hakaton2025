<template>
    <header>
        <div class="logo">
            <h1>Байтики</h1>
            <img src="../assets/header/Blogo.svg" alt="logo" />
        </div>
        <div class="user">
            <img
                src="../assets/header/проекты.svg"
                alt="projects"
                v-if="loginCheck"
            />
            <img
                src="../assets/header/профиль.svg"
                @click="toProfile"
                alt="user"
            />
        </div>
    </header>
</template>

<script>
export default {
    name: "header",
    data() {
        return {
            loginCheck: false,
        };
    },
    methods: {
        toProfile() {
            this.$router.push("/user");
        },
    },
};
</script>

<style>
header {
    display: flex;
    flex-direction: row;
    border-bottom: 1px solid #969595;
    height: 5rem;
    padding: 0 90px;
    align-items: center;
    justify-content: space-between;
}
.logo img {
    height: 2rem;
    width: 2rem;
    display: block;
}
.logo {
    display: flex;
    align-items: baseline;
    color: white;
    gap: 0.8rem;
}
h1 {
    font-weight: bold;
    font-size: 30px;
}
.user {
    display: flex;
    gap: 50px;
}
.user img {
    height: 2rem;
    width: 2rem;
    display: block;
    transition: transform 0.5s ease;
}
.user img:hover {
    transform: scale(1.3);
    cursor: pointer;
}
</style>
