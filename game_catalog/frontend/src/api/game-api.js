import axios from 'axios';

export function getGames(){
  return axios.get('/api/games')
              .then(response => response.data.results);
}
