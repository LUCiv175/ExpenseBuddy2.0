import React, { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const url = process.env.REACT_APP_API_URL;
  const [user, setUser] = useState("franco");
  useEffect(() => {
    const get_user = async () => {
      try {
        const response = await fetch(`${url}/get_current_user`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
          credentials: "include",
        });

        if (!response.ok) {
          throw new Error("Invalid response");
        }

        const json = await response.json();
        setUser(json);
      } catch (error) {
        console.log("Error:", error);
        return;
      }
    };

    get_user();
  }, []);
  const login = async (username, password) => {
    return await fetch(`${url}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          // Esci dalla catena di promesse
          throw new Error("Invalid response");
        }
        return response.json();
      })
      .then((json) => {
        setUser(json.user);
        return { message: "Loggin in", status: 200 };
      })
      .catch((error) => {
        // Se la risposta non è "ok", questa sezione verrà eseguita
        console.log("Error:", error);
        return { message: "Wrong username or Password", status: 401 };
      });
  };

  const logout = async () => {
    try {
      await fetch(`${url}/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
      });
      setUser(null);
    } catch (error) {
      console.log(error);
    }
  };

  const changePassword = async (oldPw, newPw) => {
    return await fetch(`${url}/change_password`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        new_password: newPw,
        old_password: oldPw,
      }),
      credentials: "include",
    })
      .then((response) => {
        if (!response.ok) {
          // Esci dalla catena di promesse
          throw new Error("Invalid response");
        }
        return response.json();
      })
      .then((json) => {
        setUser(json.user);
        return { message: "Password changed", status: 200 };
      })
      .catch((error) => {
        // Se la risposta non è "ok", questa sezione verrà eseguita
        console.log("Error:", error);
        return { message: "Wrong Password", status: 401 };
      });
  };

  const value = {
    user: user,
    onLogin: login,
    onLogout: logout,
    onChangePassword: changePassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
