import { Outlet, Link } from "react-router-dom";
import CustomHeader from "../components/customHeader";

const Layout = () => {
  return (
    <>
      <CustomHeader/>

      <Outlet />
    </>
  )
};

export default Layout;