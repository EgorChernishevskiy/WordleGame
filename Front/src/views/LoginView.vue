<template>
  <div class="login-register">
    <h1>{{ isLogin ? 'Вход' : 'Регистрация' }}</h1>
    <form @submit.prevent="handleSubmit">
      <container class="log">
        <div>
          <label for="username">Логин:</label>
          <input v-model="username" id="username" type="text" required />
        </div>
        <div>
          <label for="password">Пароль:</label>
          <input v-model="password" id="password" type="password" required />
        </div>
        <button type="submit">{{ isLogin ? 'Войти' : 'Зарегистрироваться' }}</button>
      </container>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p>
      <span @click="toggleForm" style="cursor: pointer;">
        {{ isLogin ? 'Нет аккаунта? Зарегистрируйтесь.' : 'Уже есть аккаунт? Войдите.' }}
      </span>
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { login, register } from '../api/auth'; // Импорт API

export default defineComponent({
  name: 'LoginRegisterView',
  setup() {
    const username = ref('');
    const password = ref('');
    const isLogin = ref(true); // Определяет, показывать форму логина или регистрации
    const errorMessage = ref<string | null>(null);

    const handleSubmit = async () => {
      try {
        errorMessage.value = null; // Сбрасываем ошибку перед запросом

        if (isLogin.value) {
          // Вход
          const token = await login(username.value, password.value);

          // Сохраняем токен и ID пользователя
          localStorage.setItem('access_token', token.access_token);
          localStorage.setItem('user_id', String(token.user_id));

          window.location.href = '/game';
        } else {
          // Регистрация
          await register({ user_name: username.value, password: password.value });
          alert('Регистрация прошла успешно! Теперь вы можете войти.');
          isLogin.value = true; // Переключаемся на логин
        }
      } catch (error: unknown) {
        if (error && typeof error === 'object' && 'response' in error) {
          const err = error as { response: { data?: { detail?: string } } };
          errorMessage.value =
            err.response.data?.detail || 'Произошла ошибка. Проверьте данные и попробуйте снова.';
          console.error('Ошибка:', err.response.data?.detail);
        } else if (error instanceof Error) {
          console.error('Ошибка:', error.message);
          errorMessage.value = error.message || 'Произошла ошибка. Проверьте данные и попробуйте снова.';
        } else {
          console.error('Неизвестная ошибка:', error);
          errorMessage.value = 'Произошла неизвестная ошибка. Попробуйте снова.';
        }
      }
    };

    const toggleForm = () => {
      isLogin.value = !isLogin.value;
    };

    return {
      username,
      password,
      isLogin,
      errorMessage,
      handleSubmit,
      toggleForm,
    };
  },
});
</script>

<style scoped>
.login-register {
  display: flex;
  flex-direction: column;
  margin: auto;
  margin-top: 200px;
  align-items: center;
  gap: 10px;
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.log {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}

button {
  width: 200px;
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #2980b9;
}
</style>
