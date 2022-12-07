import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Login from '../pages/Login';
import Page404 from '../pages/Page404';
import PrivateRoute from './PrivateRoute';
import Home from '../pages/Home';

export default function Routers() {
  return (
    <Routes>
      <Route path="/" element={<PrivateRoute />}>
        <Route path="/" element={<Home />} />
      </Route>
      <Route path="/login" element={<Login />} />
      <Route path="*" element={<Page404 />} />
    </Routes>
  );
}
