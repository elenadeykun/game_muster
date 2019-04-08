import { combineReducers } from 'redux';

import userReducer from './user-reducer';
import gameReducer from './game-reducer';

var reducers = combineReducers({
    userState: userReducer,
    gameState: gameReducer
});

export default reducers;
