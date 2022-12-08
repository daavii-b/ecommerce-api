/* eslint-disable no-console */
import React from 'react';
import { FaHome, FaSignInAlt, FaUserAlt } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { Header, H1, Nav, Ul } from './styled';

export default function MainHeader() {
  const { authReducer, emailReducer } = useSelector((state) => ({ ...state }));
  return (
    <Header>
      <H1>E-commerce</H1>
      <Nav>
        <Ul>
          <li>
            <Link to="/" state={{ isLoggedIn: true }}>
              <FaHome size={24} />
            </Link>
          </li>
          <li>
            <Link to="/login">
              <FaSignInAlt size={24} />
            </Link>
          </li>
          <li>
            <Link to="/logout">
              <FaUserAlt size={24} />
            </Link>
          </li>
          {authReducer.buttonClicked ? 'Clicked ' : 'Not Clicked'}
          {emailReducer.emailVerified ? 'Verified' : 'Not verified'}
        </Ul>
      </Nav>
    </Header>
  );
}
