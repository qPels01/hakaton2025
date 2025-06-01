<template>
  <div class="backdrop">
    <div class="modal">
      <button class="close-btn" @click="$emit('close')">×</button>
      <div class="modal-header">
        <h2>Задачи по проекту x</h2>
      </div>
      <div class="modal-body">
        <div v-for="(task, index) in tasks" :key="task.name" class="task-row">
          <span class="role">{{ task.role }}</span>
          <span class="desc">{{ task.desc }}</span>
          <span class="date">до {{ task.date }}</span>
          <button class="task-action">посмотреть описание</button>
          <span
            class="task-checkbox"
            :class="{ checked: task.status }"
            @click="toggleStatus(index)"
          ></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TasksModal",
  data() {
    return {
      tasks: [
        {
          role: "Дизайнер А",
          desc: "Подобрать цветовые решения",
          date: "31.05.25",
          status: false,
        },
        {
          role: "Дизайнер Б",
          desc: "Создать макет дизайна",
          date: "01.06.25",
          status: false,
        },
      ],
    };
  },
  methods: {
    toggleStatus(index) {
      this.tasks[index].status = !this.tasks[index].status;
    },
  },
};
</script>

<style scoped>
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal {
  background: #474a52;
  border-radius: 12px;
  border: 2px solid #3fa8ff; /* акцент */
  box-shadow: 0 4px 32px rgba(16, 32, 56, 0.4);
  padding: 36px 28px 28px 28px;
  min-width: 540px;
  width: 720px;
  max-width: 96vw;
  position: relative;
}
.modal-header {
  text-align: center;
  margin-bottom: 22px;
}
.modal-header h2 {
  margin: 0;
  font-size: 1.6rem;
  color: #fff;
  font-weight: 700;
}
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}
.task-row {
  display: flex;
  align-items: center;
  gap: 1.1rem;
  padding: 12px 0;
  border-bottom: 1px solid #3fa8ff;
  font-size: 1.1rem;
  color: #fff;
}
.task-row:last-child {
  border-bottom: none;
}
.role {
  width: 160px;
  font-weight: 500;
}
.desc {
  flex: 1;
  color: #dadada;
}
.date {
  min-width: 110px;
  color: #7fcfff;
}
.task-action {
  background: none;
  border: none;
  color: #3fa8ff;
  cursor: pointer;
  text-decoration: underline;
  font-size: 1rem;
  margin-right: 10px;
}
.task-checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #3fa8ff;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  background: none;
  cursor: pointer;
}

.task-checkbox.checked {
  background: #3fa8ff;
}
.close-btn {
  position: absolute;
  top: 22px;
  right: 32px;
  background: transparent;
  border: none;
  color: #ff4a4a;
  font-size: 2rem;
  font-weight: bold;
  cursor: pointer;
  z-index: 10;
  line-height: 1;
  padding: 0;
  transition: color 0.1s;
}
.close-btn:hover {
  color: #ff2020;
}
</style>
