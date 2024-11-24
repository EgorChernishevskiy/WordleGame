<template>
  <div class="game-container">
    <h1>Wordle</h1>

    <!-- Игровое поле -->
    <div class="grid">
      <div
        v-for="(row, rowIndex) in grid"
        :key="rowIndex"
        class="grid-row"
      >
        <div
          v-for="(cell, cellIndex) in row"
          :key="cellIndex"
          class="grid-cell"
          :class="{
            correct: cell.status === 'correct',
            present: cell.status === 'present',
            absent: cell.status === 'absent',
          }"
        >
          {{ cell.letter }}
        </div>
      </div>
    </div>

    <!-- Клавиатура -->
    <div class="keyboard">
      <div class="keyboard-row" v-for="(row, rowIndex) in keyboardRows" :key="rowIndex">
        <button
          v-for="key in row"
          :key="key"
          class="key"
          @click="handleKeyClick(key)"
          :class="{
            correct: keyStatuses[key] === 'correct',
            present: keyStatuses[key] === 'present',
            absent: keyStatuses[key] === 'absent',
          }"
        >
          {{ key }}
        </button>
      </div>
      <div class="keyboard-row">
        <button class="key special" @click="handleDelete">←</button>
        <button class="key special" @click="handleSubmit">Проверить</button>
      </div>
    </div>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="gameOver" class="game-over">
      {{ gameWon ? 'Поздравляем! Вы угадали слово!' : 'Игра окончена! Попробуйте ещё раз.' }}
    </p>
    <button v-if="gameOver" @click="startNewGame" class="new-game">Новая игра</button>
  </div>
</template>
<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { startGame, makeAttempt } from '../api/auth';
import { AttemptResult, GameStart } from '../api/auth';

export default defineComponent({
  name: 'GameView',
  setup() {
    const gameId = ref<number | null>(null);
    const grid = ref(
      Array(6)
        .fill(null)
        .map(() => Array(5).fill({ letter: '', status: '' }))
    );
    const currentRow = ref(0);
    const currentCol = ref(0);
    const keyboardRows = ref([
      ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
      ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
      ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    ]);
    const keyStatuses = ref<Record<string, string>>({});
    const loading = ref(true);
    const errorMessage = ref<string | null>(null);
    const gameOver = ref(false);
    const gameWon = ref(false);

    const startNewGame = async () => {
      try {
        loading.value = true;
        const response: GameStart = await startGame();
        gameId.value = response.game_id;
        grid.value = Array(6)
          .fill(null)
          .map(() => Array(5).fill({ letter: '', status: '' }));
        currentRow.value = 0;
        currentCol.value = 0;
        keyStatuses.value = {};
        gameOver.value = false;
        gameWon.value = false;
      } catch (error: any) {
        console.error('Ошибка при запуске игры:', error);
        errorMessage.value = error.response?.data?.detail || 'Не удалось начать игру.';
      } finally {
        loading.value = false;
      }
    };

    const handleKeyClick = (key: string) => {
      if (gameOver.value || currentCol.value >= 5) return;
      grid.value[currentRow.value][currentCol.value] = { letter: key, status: '' };
      currentCol.value++;
    };

    const handleDelete = () => {
      if (currentCol.value > 0) {
        currentCol.value--;
        grid.value[currentRow.value][currentCol.value] = { letter: '', status: '' };
      }
    };

    const handleSubmit = async () => {
      if (currentCol.value < 5 || gameOver.value) return;

      const word = grid.value[currentRow.value].map((cell) => cell.letter).join('').toLowerCase();
      try {
        const response: AttemptResult = await makeAttempt(gameId.value!, { word });
        response.correct_positions.forEach((pos) => {
          grid.value[currentRow.value][pos].status = 'correct';
          keyStatuses.value[grid.value[currentRow.value][pos].letter] = 'correct';
        });

        response.correct_letters.forEach((pos) => {
          if (grid.value[currentRow.value][pos].status !== 'correct') {
            grid.value[currentRow.value][pos].status = 'present';
            keyStatuses.value[grid.value[currentRow.value][pos].letter] = 'present';
          }
        });

        grid.value[currentRow.value].forEach((cell) => {
          if (!cell.status) {
            cell.status = 'absent';
            keyStatuses.value[cell.letter] = 'absent';
          }
        });

        gameWon.value = response.game_won;
        gameOver.value = response.game_won || response.attempts_left === 0;
        if (!gameOver.value) {
          currentRow.value++;
          currentCol.value = 0;
        }
      } catch (error: any) {
        console.error('Ошибка при отправке попытки:', error);
        errorMessage.value = error.response?.data?.detail || 'Не удалось обработать попытку.';
      }
    };

    const handleKeyPress = (event: KeyboardEvent) => {
      const key = event.key.toUpperCase();
      if (/^[A-Z]$/.test(key)) {
        handleKeyClick(key);
      } else if (key === 'BACKSPACE') {
        handleDelete();
      } else if (key === 'ENTER') {
        handleSubmit();
      }
    };

    onMounted(() => {
      window.addEventListener('keydown', handleKeyPress);
      startNewGame();
    });

    return {
      grid,
      keyboardRows,
      keyStatuses,
      currentRow,
      currentCol,
      loading,
      errorMessage,
      gameOver,
      gameWon,
      startNewGame,
      handleKeyClick,
      handleDelete,
      handleSubmit,
    };
  },
});
</script>

<style scoped>
.game-container {
  text-align: center;
  max-width: 400px;
  margin: auto;
}

.grid {
  display: grid;
  grid-template-rows: repeat(6, 50px);
  grid-gap: 5px;
  margin-bottom: 20px;
}

.grid-row {
  display: flex;
  justify-content: center;
}

.grid-cell {
  width: 50px;
  height: 50px;
  border: 1px solid #ddd;
  text-align: center;
  line-height: 50px;
  font-size: 20px;
  font-weight: bold;
  text-transform: uppercase;
}

.correct {
  background-color: #4caf50;
  color: white;
}

.present {
  background-color: #ffc107;
  color: black;
}

.absent {
  background-color: #ccc;
}

.keyboard {
  margin-top: 20px;
}

.keyboard-row {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.key {
  margin: 0 5px;
  padding: 10px 15px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-transform: uppercase;
}

.key.correct {
  background-color: #4caf50;
  color: white;
}

.key.present {
  background-color: #ffc107;
  color: black;
}

.key.absent {
  background-color: #ccc;
}

.key.special {
  background-color: #f44336;
  color: white;
}
</style>
