import React, { createContext, useState } from "react";
import type { ReactNode } from "react";
interface AuthContextType {
  token: string | null;
  setToken: (token: string | null) => void;
}

// Default context (no token initially)
export const AuthContext = createContext<AuthContextType>({
  token: null,
  setToken: () => {},
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setTokenState] = useState<string | null>(
    localStorage.getItem("token")
  );

  const setToken = (newToken: string | null) => {
    if (newToken) {
      localStorage.setItem("token", newToken);
    } else {
      localStorage.removeItem("token");
    }
    setTokenState(newToken);
  };

  return (
    <AuthContext.Provider value={{ token, setToken }}>
      {children}
    </AuthContext.Provider>
  );
};
