<template>
  <div class="gantt-outer">
    <div class="gantt-scroll">
      <div class="gantt">
        <div class="gantt-header">
          <div class="name-cell"></div>
          <div v-for="day in allDates" :key="day" class="header-cell">
            {{ day }}
          </div>
        </div>
        <div v-for="team in teams" :key="team.name" class="gantt-row">
          <div @click="toggleModal()" class="name-cell">
            {{ team.name }}
          </div>
          <div class="row-content">
            <div
              v-for="task in team.tasks"
              :key="task.name"
              class="task"
              :style="getTaskStyle(task)"
            >
              {{ task.name }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <TeamLog v-if="showModal" @close="showModal = false" />
  </div>
</template>

<script>
import TeamLog from "./modals/TeamLog.vue";

function genDays(start, end) {
  const arr = [];
  let dt = new Date(start);
  end = new Date(end);
  while (dt <= end) {
    arr.push(dt.toISOString().slice(0, 10));
    dt.setDate(dt.getDate() + 1);
  }
  return arr;
}

export default {
  components: { TeamLog },
  data() {
    return {
      showModal: false,
      rawTeams: [
        {
          name: "Команда 1",
          tasks: [
            {
              name: "проект x",
              start_date: "2025-05-31T08:36:55.435114",
              end_date: "2025-06-01T20:36:55.435114",
              color: "#f68926",
            },
          ],
        },
        {
          name: "Команда 2",
          tasks: [
            {
              name: "проект y",
              start_date: "2025-06-03",
              end_date: "2025-06-04",
              color: "#b85fa5",
            },
          ],
        },
      ],
    };
  },
  computed: {
    allDates() {
      // Собираем все start_date и end_date
      const dates = this.rawTeams.flatMap((team) =>
        team.tasks.flatMap((task) => [
          task.start_date.slice(0, 10),
          task.end_date.slice(0, 10),
        ])
      );
      // Выбираем min и max
      const min = dates.reduce((a, b) => (a < b ? a : b));
      const max = dates.reduce((a, b) => (a > b ? a : b));
      return genDays(min, max);
    },
    teams() {
      return this.rawTeams.map((team) => ({
        name: team.name,
        tasks: team.tasks
          .map((task) => {
            const formatDate = (d) => d.slice(0, 10);
            const start = this.allDates.indexOf(formatDate(task.start_date));
            const end = this.allDates.indexOf(formatDate(task.end_date));
            if (start === -1 || end === -1) return null;
            return {
              ...task,
              start,
              duration: end - start + 1,
            };
          })
          .filter(Boolean),
      }));
    },
  },
  methods: {
    getTaskStyle(task) {
      return {
        left: `calc(${task.start} * 140px)`,
        width: `calc(${task.duration} * 140px)`,
        background: task.color,
      };
    },
    toggleModal() {
      this.showModal = !this.showModal;
    },
  },
};
</script>

<!-- стиль как у тебя, исправлений не требует -->
<style scoped>
.gantt-outer {
  background: #2b2d32;
  height: max-content;
  box-sizing: border-box;
  width: 100%;
  margin: 40px auto;
}

.gantt-scroll {
  overflow-x: auto;
  background: #43464d;
  border-radius: 18px;
  padding: 8px 0;
}
.gantt {
  min-width: 700px;
  min-width: fit-content;
  padding: 20px;
}
.gantt-header {
  display: flex;
  border-bottom: 2px solid #ccc;
  color: white;
}
.gantt-row {
  display: flex;
  border-bottom: 1px solid #86878e;
  align-items: center;
  height: 48px;
}
.name-cell {
  width: 150px;
  min-width: 150px;
  padding: 8px;
  font-size: 18px;
  background: transparent;
  border-right: 1px solid #86878e;
  display: flex;
  align-items: center;
  color: white;
  cursor: pointer;
}
.name-cell:hover {
  background: #86878e;
  border-radius: 5px;
}
.header-cell {
  width: 140px;
  min-width: 140px;
  text-align: center;
  padding: 4px 0;
  border-right: 1px solid #86878e;
  font-weight: 600;
}
.row-content {
  position: relative;
  flex: 1;
  min-width: 0;
  height: 100%;
}
.task {
  position: absolute;
  top: 8px;
  height: 32px;
  border-radius: 4px;
  color: #fff;
  padding: 0 14px;
  display: flex;
  align-items: center;
  font-size: 16px;
  font-weight: 500;
  z-index: 1;
  white-space: nowrap;
  box-sizing: border-box;
}
.gantt-scroll::-webkit-scrollbar {
  height: 8px;
  background: #393b40;
  border-radius: 8px;
}
.gantt-scroll::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 8px;
}
.gantt-scroll::-webkit-scrollbar-thumb:hover {
  background: #b2b2b2;
}
.gantt-scroll {
  scrollbar-color: #888 #393b40;
  scrollbar-width: thin;
}
</style>
