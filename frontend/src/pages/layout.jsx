import { Outlet, Link } from "react-router-dom";
import CustomHeader from "../components/CustomHeader";

const Layout = () => {
  return (
    <>
      <CustomHeader />

      <Outlet />
    </>
  );
};

export default Layout;
