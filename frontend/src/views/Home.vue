<script>
export default {
  name: "home",
  data() {
    return {
      isVisible: false,
    };
  },
  mounted() {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          this.isVisible = true;
          observer.unobserve(this.$el);
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(this.$el.querySelector(".discription"));
  },
  methods: {
    toRegister() {
      this.$router.push("/register");
    },
    toLogin() {
      this.$router.push("/login");
    },
  },
};
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
      <button @click="toLogin">Войти</button>
    </section>
    <section class="section-2">
      <div class="discription">
        <div class="disc-text" :class="{ 'fade-in': true, visible: isVisible }">
          <h1>Скорость</h1>
          <p>
            У нас большой штат сотрудников, разделённый на множество команд.
            Поэтому работа будет идти быстро
          </p>
        </div>
        <div class="disc-text" :class="{ 'fade-in': true, visible: isVisible }">
          <h1>Качество</h1>
          <p>
            Наши специалисты обладают огромным опытом, что способствует
            качественной работе
          </p>
        </div>
        <div class="disc-text" :class="{ 'fade-in': true, visible: isVisible }">
          <h1>Цена-качество</h1>
          <p>
            Наша организация, гаранитирует вам качественный продукт за
            соответствующую цену
          </p>
        </div>
      </div>
      <div class="register" :class="{ 'fade-in': true, visible: isVisible }">
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
  font-size: 3.5rem;
  letter-spacing: 0.15rem;
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
  font-size: 2rem;
  font-weight: bold;
}
.disc-text p {
  white-space: normal;
  word-wrap: break-word;
}
.register {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 0.5em;
}
.register button {
  max-width: 20rem;
  margin: 0 0;
}
</style>
