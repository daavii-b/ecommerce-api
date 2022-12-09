/* eslint-disable no-console */
import * as types from '../types';

export default (state = {}, action) => {
  switch (action.type) {
    case types.LOGIN_BUTTON_SUCCESS: {
      const newState = { ...state };
      console.log('Successfully logged in');
      newState.buttonClicked = !newState.buttonClicked;
      return newState;
    }
    case types.LOGIN_BUTTON_FAILURE: {
      console.log('Failed to log in');

      return state;
    }
    case types.LOGIN_BUTTON_REQUEST: {
      console.log('Requesting login');
      return state;
    }
    default:
      return state;
  }
};
