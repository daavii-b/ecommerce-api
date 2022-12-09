import * as types from '../types';

export default (state = {}, action) => {
  switch (action.type) {
    case types.LOGIN_BUTTON_SUCCESS: {
      const newState = { ...state };

      newState.emailVerified = !newState.emailVerified;
      return newState;
    }

    default:
      return state;
  }
};
