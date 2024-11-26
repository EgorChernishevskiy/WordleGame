import { createRouter, createWebHistory, RouteLocationNormalized, NavigationGuardNext } from 'vue-router';
import LoginPage from '../views/LoginView.vue';
import GamePage from '../views/GameView.vue';
import TopPlayersPage from '../views/TopPlayersView.vue';
import ProfilePage from '../views/ProfileView.vue';
import { isAuthenticated } from '../api/auth';


const routes = [
  {
    path: '/',
    name: 'Login',
    component: LoginPage,
    beforeEnter: (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
      if (isAuthenticated()) {
        next({ name: 'Game' });
      } else {
        next();
      }
    },
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
    beforeEnter: (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
      if (!isAuthenticated()) {
        next({ name: 'Login' });
      } else {
        next();
      }
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
