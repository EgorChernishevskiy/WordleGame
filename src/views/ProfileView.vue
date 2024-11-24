<template>
  <div>
    <h1>Профиль</h1>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>
    <div v-else>
      <p><strong>Имя пользователя:</strong> {{ user.user_name }}</p>
      <p><strong>Победы:</strong> {{ user.wins }}</p>
      <p><strong>Процент W/L:</strong> {{ (user.win_rate * 100).toFixed(2) }}%</p>
      <p><strong>Ранг по победам:</strong> {{ user.rank_by_wins }}</p>
      <p><strong>Ранг по W/L:</strong> {{ user.rank_by_win_rate ?? 'Не в рейтинге' }}</p>
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
.error {
  color: red;
  font-weight: bold;
  margin-top: 20px;
}
</style>
