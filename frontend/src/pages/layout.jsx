import { Outlet, Link } from "react-router-dom";
import CustomHeader from "../components/CustomHeader";
import GroupContextProvider from "../contexts/GroupContext";
import { CookiesProvider, useCookies } from "react-cookie";

const Layout = () => {
  const [cookies, setCookie] = useCookies(["selectedGroup"]);
  const handleGroupChange = (groupIndex) => {
    setCookie("selectedGroup", groupIndex, { path: "/" });
  };

  return (
    <>
      <CookiesProvider>
        <GroupContextProvider selectedCookieGroup={cookies.selectedGroup}>
          <CustomHeader onGroupChange={handleGroupChange} />

          <Outlet />
        </GroupContextProvider>
      </CookiesProvider>
    </>
  );
};

export default Layout;
