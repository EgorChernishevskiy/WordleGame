<template>
  <div>
    <h1>Профиль</h1>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>
    <div v-else>
      <table class="profile-table">
        <thead>
          <tr>
            <th>Параметр</th>
            <th>Значение</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Имя пользователя</strong></td>
            <td>{{ user.user_name }}</td>
          </tr>
          <tr>
            <td><strong>Победы</strong></td>
            <td>{{ user.wins }}</td>
          </tr>
          <tr>
            <td><strong>Процент W/L</strong></td>
            <td>{{ (user.win_rate * 100).toFixed(2) }}%</td>
          </tr>
          <tr>
            <td><strong>Ранг по победам</strong></td>
            <td>{{ user.rank_by_wins }}</td>
          </tr>
          <tr>
            <td><strong>Ранг по W/L</strong></td>
            <td>{{ user.rank_by_win_rate ?? 'Не в рейтинге' }}</td>
          </tr>
        </tbody>
      </table>
      <div class="exit">
        <button class="but-ex">Выход</button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { getUserScore, getCurrentUserId, CurrentUser } from '../api/auth';

export default defineComponent({
  name: 'ProfilePage',
  setup() {
    // Инициализируем `user` с соответствующим типом CurrentUser
    const user = ref<CurrentUser>({
      user_name: '',
      wins: 0,
      win_rate: 0.0,
      rank_by_wins: null,
      rank_by_win_rate: null,
    });

    const loading = ref(true);
    const errorMessage = ref<string | null>(null);

    onMounted(async () => {
      try {
        const userId = getCurrentUserId();
        if (!userId) {
          throw new Error('Пользователь не авторизован');
        }
        // Запрашиваем данные текущего пользователя
        const response = await getUserScore(userId);
        // Обновляем данные пользователя
        user.value = response;
      } catch (error: any) {
        console.error('Ошибка при загрузке данных профиля:', error);
        errorMessage.value =
          error.response?.data?.detail || 'Не удалось загрузить данные профиля.';
      } finally {
        loading.value = false;
      }
    });

    return { user, loading, errorMessage };
  },
});
</script>

<style scoped>
h1 {
  display: flex;
  justify-content: center;
  margin-top: 70px;
}

.profile-table {
  width: 80%;
  margin: 50px auto;
  border-collapse: collapse;
  text-align: left;
}

.profile-table th,
.profile-table td {
  border: 1px solid #0093b8;
  padding: 8px;
}

.profile-table th {
  background-color: #00eeff;
  text-align: center;
}

.profile-table tr:hover {
  background-color: #f1f1f1;
}

.exit {
  display: flex;
  justify-content: center;
}

.but-ex {
  width: 100px;
  height: 40px;
  background-color: #0093b8;
  color: white;
  border-radius: 20px;
  border: 1px solid #000;
  cursor: pointer;
  transition: color .18s ease-in-out;
}

.but-ex:hover {
  background-color: #00eeff;
  color: #000;
}

.error {
  color: red;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
}
</style>
