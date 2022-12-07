import React from 'react';
import { FaSadCry } from 'react-icons/fa';
import { Container } from '../../styles/GlobalStyles';

export default function Page404() {
  return (
    <Container>
      <h2>404 - Page not Found</h2> <FaSadCry />
    </Container>
  );
}
