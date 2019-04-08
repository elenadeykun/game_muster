import * as types from '../actions/action-types';

export function getGamesSuccess(games) {
  return {
    type: types.GET_GAMES_SUCCESS,
    games
  };
}
