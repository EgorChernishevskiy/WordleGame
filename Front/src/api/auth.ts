import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface UserCreate {
  user_name: string;
  password: string;
}

export interface TopPlayer {
  user_name: string;
  wins: number;
  win_rate: number;
  games_played: number;
}

export interface CurrentUser {
  user_name: string;
  wins: number;
  win_rate: number;
  rank_by_wins: number | null;
  rank_by_win_rate: number | null;
}

export interface Token {
  access_token: string;
  token_type: string;
  user_id: number;
}

export interface Attempt {
  word: string;
}

export interface AttemptResult {
  word: string;
  correct_positions: number[];
  correct_letters: number[];
  attempts_left: number;
  game_won: boolean;
}

export interface GameStart {
  game_id: number;
  is_active: boolean;
}

export const register = async (user: UserCreate): Promise<void> => {
  await api.post('/register', user);
};

// Функция входа
export const login = async (username: string, password: string): Promise<Token> => {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);

  const response = await api.post('/login', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  return response.data;
};

export const startGame = async (): Promise<GameStart> => {
  const headers: Record<string, string> = {};

  const token = localStorage.getItem('access_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await api.post('/game/game/start', null, { headers });
  return response.data;
};

export const makeAttempt = async (
  gameId: number,
  attempt: Attempt
): Promise<AttemptResult> => {
  const headers: Record<string, string> = {};

  const token = localStorage.getItem('access_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await api.post(`/game/game/${gameId}/attempt`, attempt, { headers });
  return response.data;
};

export const getTopPlayers = async (): Promise<{
  top_by_win_rate: TopPlayer[];
  top_by_wins: TopPlayer[];
}> => {
  const response = await api.get('/users/top');
  return response.data;
};

export const getUserScore = async (userId: number): Promise<CurrentUser> => {
  const response = await api.get(`/users/user/${userId}/score`);
  const data = response.data.data;
  return {
    user_name: data.user_name,
    wins: data.wins,
    win_rate: data.win_rate,
    rank_by_wins: data.rank_by_wins,
    rank_by_win_rate: data.rank_by_win_rate,
  };
};

export const getCurrentUserId = (): number | null => {
  const userId = localStorage.getItem('user_id');
  return userId ? Number(userId) : null;
};

export const isAuthenticated = () => {
  return getCurrentUserId() !== null; 
};

export const logout = () => {
  localStorage.removeItem('user_id');
  localStorage.removeItem('access_token');
};