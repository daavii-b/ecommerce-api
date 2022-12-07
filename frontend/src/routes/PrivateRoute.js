import React from 'react';
import { Navigate, useLocation, Outlet } from 'react-router-dom';

export default function PrivateRoute() {
  const location = useLocation();
  const { isLoggedIn } = location.state || false;

  return !isLoggedIn ? (
    <Navigate to="/login" state={location.pathname} replace />
  ) : (
    <Outlet />
  );
}
