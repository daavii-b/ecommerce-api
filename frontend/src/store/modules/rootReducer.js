import authReducer from './auth/reducer';
import emailReducer from './email/reducer';

export const initialState = {
  authReducer: { buttonClicked: false },
  emailReducer: { emailVerified: false },
};

export default {
  authReducer,
  emailReducer,
};
