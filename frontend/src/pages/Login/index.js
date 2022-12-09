import React from 'react';
import { useDispatch } from 'react-redux';
import { H2, P } from './styled';
import { Container } from '../../styles/GlobalStyles';
import * as userActions from '../../store/modules/auth/actions';

export default function Login() {
  const dispatch = useDispatch();

  function handleClick(e) {
    e.preventDefault();

    dispatch(userActions.loginButtonRequest());
  }

  return (
    <Container>
      <H2>Login Page</H2>
      <P>
        Lorem, ipsum dolor sit amet consectetur adipisicing elit. Dolores
        commodi, suscipit quis illo itaque odio aperiam voluptate vero
        consequatur consectetur ad veritatis labore accusantium aut cupiditate
        ex, aspernatur iure laborum?
      </P>

      <button type="button" onClick={handleClick}>
        Send
      </button>
    </Container>
  );
}
