import { createContext, useState } from "react";
import { ReactNode } from "react";

const AuthContext = createContext({
  loggedIn: false,
  setLoggedIn: (loggedIn: boolean) => {},
});

interface Props {
  children: ReactNode;
}

export const AuthProvider = ({ children }: Props) => {
  const [loggedIn, setLoggedIn] = useState(false);
  return (
    <AuthContext.Provider value={{ loggedIn, setLoggedIn }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
