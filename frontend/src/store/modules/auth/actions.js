import * as types from '../types';

export function loginButtonRequest() {
  return {
    type: types.LOGIN_BUTTON_REQUEST,
  };
}

export function loginButtonSuccess() {
  return {
    type: types.LOGIN_BUTTON_SUCCESS,
  };
}

export function loginButtonFailure() {
  return {
    type: types.LOGIN_BUTTON_FAILURE,
  };
}
