import { createContext, useState } from "react";
import { ReactNode } from "react";

const AuthContext = createContext({
  loggedIn: false,
  setLoggedIn: (loggedIn: boolean) => { console.log(loggedIn) },
  userName: "",
  // setUserName is a function that takes a string and returns nothing
  setUserName: (userName: string) => { console.log(userName) },
});

interface Props {
  children: ReactNode;
}

export const AuthProvider = ({ children }: Props) => {
  const [loggedIn, setLoggedIn] = useState(false);
  const [userName, setUserName] = useState("");
  return (
    <AuthContext.Provider value={{ loggedIn, setLoggedIn, userName, setUserName }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
