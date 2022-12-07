/* eslint-disable jsx-a11y/anchor-is-valid */
import React from 'react';
import { FaHome, FaSignInAlt, FaUserAlt } from 'react-icons/fa';
import { Header, H1, Nav, Ul } from './styled';

export default function MainHeader() {
  return (
    <Header>
      <H1>E-commerce</H1>
      <Nav>
        <Ul>
          <li>
            <a href="#">
              <FaHome />
            </a>
          </li>
          <li>
            <a href="#">
              <FaSignInAlt />
            </a>
          </li>
          <li>
            <a href="#">
              <FaUserAlt />
            </a>
          </li>
        </Ul>
      </Nav>
    </Header>
  );
}
