<template>
  <div class="top-players">
    <h1>Рейтинги игроков</h1>

    <!-- Выбор между двумя таблицами -->
    <div class="tabs">
      <button
        :class="{ active: selectedTab === 'winrate' }"
        @click="selectedTab = 'winrate'"
      >
        Топ по W/L
      </button>
      <button
        :class="{ active: selectedTab === 'wins' }"
        @click="selectedTab = 'wins'"
      >
        Топ по Победам
      </button>
    </div>

    <!-- Таблица рейтинга -->
    <table v-if="selectedTab === 'winrate'" class="ranking-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Имя</th>
          <th>W/L (%)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(player, index) in topByWinRate" :key="player.user_name">
          <td>{{ index + 1 }}</td>
          <td>{{ player.user_name }}</td>
          <td>{{ (player.win_rate * 100).toFixed(2) }}</td>
        </tr>
        <tr v-if="currentUser && !isInTopWinRate" class="current-user-row">
          <td colspan="4" class="separator">...</td>
        </tr>
        <tr v-if="currentUser && !isInTopWinRate" :class="{ highlight: true }">
          <td>{{ currentUser.rank_by_win_rate ?? '—' }}</td>
          <td>{{ currentUser.user_name }}</td>
          <td>{{ (currentUser.win_rate * 100).toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>

    <table v-if="selectedTab === 'wins'" class="ranking-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Имя</th>
          <th>Победы</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(player, index) in topByWins" :key="player.user_name">
          <td>{{ index + 1 }}</td>
          <td>{{ player.user_name }}</td>
          <td>{{ player.wins }}</td>
        </tr>
        <tr v-if="currentUser && !isInTopWins" class="current-user-row">
          <td colspan="4" class="separator">...</td>
        </tr>
        <tr v-if="currentUser && !isInTopWins" :class="{ highlight: true }">
          <td>{{ currentUser.rank_by_wins ?? '—' }}</td>
          <td>{{ currentUser.user_name }}</td>
          <td>{{ currentUser.wins }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="loading">Загрузка данных...</p>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>


<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { getTopPlayers, getUserScore, getCurrentUserId } from '../api/auth';
import { TopPlayer, CurrentUser } from '../api/auth';

export default defineComponent({
  name: 'TopPlayersView',
  setup() {
    const selectedTab = ref<'winrate' | 'wins'>('winrate');
    const topByWinRate = ref<TopPlayer[]>([]);
    const topByWins = ref<TopPlayer[]>([]);
    const currentUser = ref<CurrentUser | null>(null);
    const isInTopWinRate = ref(false);
    const isInTopWins = ref(false);
    const loading = ref(true);
    const errorMessage = ref<string | null>(null);

    const fetchTopPlayers = async () => {
      try {
        loading.value = true;
        errorMessage.value = null;

        const topData = await getTopPlayers();
        topByWinRate.value = topData.top_by_win_rate;
        topByWins.value = topData.top_by_wins;

        const userId = getCurrentUserId();
        if (userId) {
          const userResponse = await getUserScore(userId);
          currentUser.value = {
            user_name: userResponse.user_name,
            wins: userResponse.wins,
            win_rate: userResponse.win_rate,
            rank_by_wins: userResponse.rank_by_wins,
            rank_by_win_rate: userResponse.rank_by_win_rate,
          };
          
          isInTopWinRate.value = topByWinRate.value.some(
            (player) => player.user_name === currentUser.value?.user_name
          );
          isInTopWins.value = topByWins.value.some(
            (player) => player.user_name === currentUser.value?.user_name
          );
        }
      } catch (error: unknown) {
        if (error && typeof error === 'object' && 'response' in error) {
          const err = error as { response: { data?: { detail?: string } } };
          console.error('Ошибка:', err.response.data?.detail || 'Неизвестная ошибка от сервера.');
          errorMessage.value =
            err.response.data?.detail || 'Не удалось загрузить данные о топ-игроках.';
        } else if (error instanceof Error) {
          console.error('Ошибка:', error.message);
          errorMessage.value = error.message || 'Не удалось загрузить данные о топ-игроках.';
        } else {
          console.error('Неизвестная ошибка:', error);
          errorMessage.value = 'Не удалось загрузить данные о топ-игроках из-за неизвестной ошибки.';
        }
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchTopPlayers();
    });

    return {
      selectedTab,
      topByWinRate,
      topByWins,
      currentUser,
      isInTopWinRate,
      isInTopWins,
      loading,
      errorMessage,
    };
  },
});
</script>

<style scoped>

h1 {
  margin-top: 70px;
}

.top-players {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 20px;
  margin: 0 10px;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
}

.tabs button.active {
  background-color: #3498db;
  color: white;
}

.ranking-table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

.ranking-table th,
.ranking-table td {
  border: 1px solid #ddd;
  text-align: center;
  padding: 8px;
}

.ranking-table th {
  background-color: #3498db;
  color: white;
}

.current-user {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.error {
  color: red;
  text-align: center;
  margin-top: 20px;
}
</style>
