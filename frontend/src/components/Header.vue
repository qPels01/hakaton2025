<template>
  <header>
    <div @click="toHome" class="logo">
      <h1>Байтики</h1>
      <img src="../assets/header/Blogo.svg" alt="logo" />
    </div>
    <div class="user" v-if="loginCheck">
      <span class="username" v-if="userName">{{ userName }}</span>
      <img src="../assets/header/профиль.svg" @click="toProfile" alt="user" />
    </div>
    <div class="user" v-else>
      <img src="../assets/header/профиль.svg" @click="toProfile" alt="user" />
    </div>
  </header>
</template>

<script>
import { jwtDecode } from "jwt-decode";
export default {
  name: "header",
  data() {
    return {
      loginCheck: false,
      userName: "",
    };
  },
  mounted() {
    this.refreshUser();
    window.addEventListener('storage', this.refreshUser);
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.refreshUser);
  },
  methods: {
  toProfile() { this.$router.push("/user"); },
  toHome() { this.$router.push("/"); },
  refreshUser() {
    const token = localStorage.getItem("jwt_token");
    this.loginCheck = !!token;
    if (token) {
      try {
        const decoded = jwtDecode(token);
        this.userName = decoded.username || decoded.name || decoded.email || '';
      } catch { this.userName = ""; }
    } else {
      this.userName = "";
    }
  }
}
};
</script>

<style>
.username {
color: #fafafc;
  font-size: 1.2rem;
  font-weight: 600;
  margin-right: 4px;
  /* cursor: pointer; */
  transition: text-decoration 0.2s;

    user-select: none;           /* вот эта строка делает текст невыделяемым */
  -webkit-user-select: none;   /* для Chrome/Safari */
  -moz-user-select: none;      /* для Firefox */
  -ms-user-select: none;       /* для IE/Edge */
}
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
  cursor: pointer;
  transition: transform 0.5s ease;
}
.logo:hover {
  transform: scale(1.1);
}
h1 {
  font-weight: bold;
  font-size: 30px;
}
.user {
  display: flex;
  align-items: center;
  gap: 6px;
}
.user img {
  height: 2rem;
  width: 2rem;
  display: block;
  transition: transform 0.5s ease;
}
.user img:hover {
  /* transform: scale(1.3); */
  cursor: pointer;
}
</style>