import * as types from '../actions/action-types';
import _ from 'lodash';

const initialState = {
  games: []
};

const gameReducer = function(state = initialState, action) {

  switch(action.type) {

    case types.GET_GAMES_SUCCESS:
      return Object.assign({}, state, { games: action.games });

  }

  return state;
}

export default gameReducer;
