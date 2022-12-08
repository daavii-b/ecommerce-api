import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';

import { ToastContainer } from 'react-toastify';
import history from './services/history';
import GlobalStyles from './styles/GlobalStyles';
import Header from './components/Header';
import Routers from './routes';

function App() {
  return (
    <Router history={history}>
      <Header />
      <Routers />
      <GlobalStyles />
      <ToastContainer autoClose={3000} />
    </Router>
  );
}

export default App;
