/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { FaHome, FaSignInAlt, FaUserAlt } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import { Header, H1, Nav, Ul } from './styled';

export default function MainHeader() {
  return (
    <Header>
      <H1>E-commerce</H1>
      <Nav>
        <Ul>
          <li>
            <Link to="/">
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
        </Ul>
      </Nav>
    </Header>
  );
}
