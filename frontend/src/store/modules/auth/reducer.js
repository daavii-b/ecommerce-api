import * as types from '../types';

export default (state = {}, action) => {
  switch (action.type) {
    case types.LOGIN_BUTTON_CLICKED: {
      const newState = { ...state };

      newState.buttonClicked = !newState.buttonClicked;
      return newState;
    }
    default:
      return state;
  }
};
