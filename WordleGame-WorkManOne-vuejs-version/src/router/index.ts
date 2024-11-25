import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../views/LoginView.vue';
import GamePage from '../views/GameView.vue';
import TopPlayersPage from '../views/TopPlayersView.vue';
import ProfilePage from '../views/ProfileView.vue';

const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage,
  },
  {
    path: '/game',
    name: 'Game',
    component: GamePage,
  },
  {
    path: '/top-players',
    name: 'TopPlayers',
    component: TopPlayersPage,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfilePage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
