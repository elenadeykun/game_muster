import * as types from '../actions/action-types';

export function getUserSuccess(user) {
  return {
    type: types.GET_USER_SUCCESS,
    user
  };
}
