import styled, { createGlobalStyle } from 'styled-components';
import 'react-toastify/dist/ReactToastify.css';

export default createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    outline: 0;
    box-sizing: border-box;
    text-decoration: none;
  }

  html {
    font-size: 62.5%;
  }

  body {
    font-family: monospace;
    font-size: 1.6rem;
  }

  html, body, #root {
    height: 100%;
  }

  button {
    cursor: pointer;
  }

  li {
    list-style-type: none;
  }

  a {
    color: inherit;
  }

  body .Toastify .Toastify__toast-container .Toastify__toast--success {
    background: transparent;
    color: green;
  }

  body .Toastify .Toastify__toast-container .Toastify__toast--error {
    background: transparent;
    color: red;

  }
`;

export const Container = styled.section`
  max-width: 89rem;
  margin: 3.6rem auto;
  background-color: grey;
  padding: 3.6rem;
  border-radius: 0.5rem;
  box-shadow: 0 0 7px 2px rgba(0, 0, 0, 0.2);
`;
