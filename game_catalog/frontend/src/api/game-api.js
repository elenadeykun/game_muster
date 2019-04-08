import axios from 'axios';
import store from '../store';
import { getGamesSuccess } from '../actions/game-actions';

export function getGames(){
  return axios.get('/api/games')
              .then(response => {
                store.dispatch(getGamesSuccess(response.data.results));
                return response;
              });
}

export function getGame(gameId){
  return axios.get('/api/games/' + gameId)
              .then(response => response.data);              
}
