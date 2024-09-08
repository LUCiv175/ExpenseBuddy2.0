import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./pages/layout";
import Home from "./pages/home";
import Login from "./pages/login";
import GroupContextProvider from "./contexts/GroupContext";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { CookiesProvider, useCookies } from "react-cookie";

export default function App() {
  const [cookies, setCookie] = useCookies(["selectedGroup"]);
  const { user } = useAuth();

  return (
    <CookiesProvider>
      <AuthProvider>
        <GroupContextProvider selectedCookieGroup={cookies.selectedGroup}>
          <BrowserRouter>
            <Routes>
              {user ? (
                <Route path="/" element={<Layout />}>
                  <Route index element={<Home />} />
                  {/* <Route path="blogs" element={<Blogs />} />
                    <Route path="contact" element={<Contact />} />
                    <Route path="*" element={<NoPage />} /> */}
                </Route>
              ) : (
                <Route path="*" element={<Login />} />
              )}
            </Routes>
          </BrowserRouter>
        </GroupContextProvider>
      </AuthProvider>
    </CookiesProvider>
  );
}
