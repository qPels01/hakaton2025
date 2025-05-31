<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isVisible = ref(false)

// Проверяем авторизацию: есть ли токен
const isAuth = ref(localStorage.getItem('jwt_token') !== null)

function toRegister() {
  router.push('/register')
}
function toLogin() {
  router.push('/login')
}
function toCabinet() {
  router.push('/user')
}

window.addEventListener('storage', () => {
  isAuth.value = localStorage.getItem('jwt_token') !== null
})

onMounted(() => {
  const el = document.querySelector('.discription')
  if (!el) return
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true
        observer.unobserve(el)
      }
    },
    { threshold: 0.1 }
  )
  observer.observe(el)
})
</script>

<template>
  <div class="home">
    <section class="section-1">
      <div class="main-font">
        <h1>
          Мы реализуем ваши <br />
          проекты
        </h1>
        <p>Легко, быстро, без проблем</p>
      </div>
      <button v-if="!isAuth" @click="toLogin">Войти</button>
      <button v-else @click="toCabinet">Перейти в личный кабинет</button>
    </section>
    <section class="section-2">
      <div class="discription">
        <div
          class="disc-text"
          :class="{ 'fade-in': true, visible: isVisible }"
        >
          <h1>Скорость</h1>
          <p>
            У нас большой штат сотрудников, разделённый на множество команд. Поэтому работа будет идти быстро
          </p>
        </div>
        <div
          class="disc-text"
          :class="{ 'fade-in': true, visible: isVisible }"
        >
          <h1>Качество</h1>
          <p>
            Наши специалисты обладают огромным опытом, что способствует качественной работе
          </p>
        </div>
        <div
          class="disc-text"
          :class="{ 'fade-in': true, visible: isVisible }"
        >
          <h1>Цена-качество</h1>
          <p>
            Наша организация, гаранитирует вам качественный продукт за соответствующую цену
          </p>
        </div>
      </div>
      <div
        v-if="!isAuth"
        class="register"
        :class="{ 'fade-in': true, visible: isVisible }"
      >
        <h1>
          Зарегистрируйтесь, чтобы иметь доступ ко всем <br />
          функциям
        </h1>
        <button @click="toRegister">Зарегистрироваться</button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
    display: flex;
    flex-direction: column;
    gap: 14.75rem;
    margin: 90px 90px;
}
.section-1 {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    gap: 100px;
}
.main-font h1 {
    background: linear-gradient(to right, #ffffff, #548dff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
    font-size: 5rem;
}
.main-font p {
    color: #979797;
    font-size: 2.5rem;
}
.section-1 button {
    border-radius: 50px;
    background: #548dff;
    border: none;
    color: #ffffff;
    width: 30.625rem;
    height: 6.5rem;
    font-size: 40px;
    transition: transform 0.5s ease;
}
.section-1 button:hover {
    background: #497bdf;
    cursor: pointer;
    transform: scale(1.1);
}
.section-2 {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
    gap: 9.25rem;
}
.discription {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-direction: row;
    align-items: center;
}
.disc-text {
    width: 20.125rem;
    height: 17.5rem;
    opacity: 0;
}
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}
.fade-in.visible {
    opacity: 2;
    transform: translateY(0);
}
.disc-text h1 {
    color: #ffffff;
    font-size: 30px;
    font-weight: bold;
}
.disc-text p {
    color: #979797;
    font-size: 30px;
    white-space: normal;
    word-wrap: break-word;
}
.register {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    gap: 20px;
}
.register h1 {
    font-size: 40px;
    font-weight: bold;
    color: #ffffff;
}
.register button {
    width: 43.75rem;
    height: 7.5rem;
    background: #548dff;
    color: white;
    border: none;
    border-radius: 50px;
    font-size: 50px;
    transition: transform 0.5s ease;
}
.register button:hover {
    background: #497bdf;
    cursor: pointer;
    transform: scale(1.1);
}
</style>
