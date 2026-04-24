import { createRoot } from "react-dom/client";
import { ThemeProvider, createGlobalStyle } from "styled-components";
import { styleReset } from "react95";
import { original } from "react95/dist/themes";
import App from "./App";

const GlobalStyles = createGlobalStyle`
  ${styleReset}
  body { background: teal; font-family: 'ms_sans_serif', sans-serif; }
`;

createRoot(document.getElementById("root")).render(
  <ThemeProvider theme={original}>
    <GlobalStyles />
    <App />
  </ThemeProvider>,
);
