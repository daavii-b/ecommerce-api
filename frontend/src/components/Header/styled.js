import styled from 'styled-components';

export const Header = styled.header`
  width: 100%;
  padding: 1rem;
`;

export const H1 = styled.h1`
  font-size: 4rem;
  color: black;
`;

export const Nav = styled.nav`
  width: 60%;
  padding: 0.6rem;
  margin: 0 auto;
`;

export const Ul = styled.ul`
  display: flex;
  align-items: center;
  justify-content: space-between;

  li {
    margin: 0 0.3rem;
  }
  a {
    display: block;
    padding: 0.6rem;
  }
`;
