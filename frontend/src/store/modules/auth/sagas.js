/* eslint-disable no-unused-vars */
/* eslint-disable no-console */
import { call, put, all, takeLatest } from 'redux-saga/effects';
import { toast } from 'react-toastify';
import * as actions from './actions';
import * as types from '../types';

const request = () =>
  new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve();
    }, 2000);
  });

function* exampleRequest() {
  try {
    yield call(request);
    toast.success('You are logged in!');
    yield put(actions.loginButtonSuccess());
  } catch (err) {
    toast.error('happened error');
    yield put(actions.loginButtonFailure());
  }
}

export default all([takeLatest(types.LOGIN_BUTTON_REQUEST, exampleRequest)]);
