<template>
  <div id="app">
    <nav>
      <router-link to="/game">Игра</router-link> |
      <router-link to="/top-players">Топ игроков</router-link> |
      <router-link to="/profile">Профиль</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

<style>
nav {
  margin-bottom: 20px;
}
nav a {
  margin: 0 10px;
  text-decoration: none;
}
</style>
