import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Home from "./components/Home/Home";
import Login from "./components/UserAuth/Login";
import Signup from "./components/UserAuth/Signup";
import UploadPortal from "./components/UserPortal/UploadPortal";
import Display from "./components/UserPortal/Display";

const Router = () => {
    const router = createBrowserRouter([
        {
            path: "/",
            element: <Home />,
        },

        {
            path: "/login",
            element: <Login />,
        },
        {
            path: "/signup",
            element: <Signup />,
        },
        {
            path: "/upload",
            element: <UploadPortal />,
        },
        {
            path: "/display",
            element: <Display />,
        },
    ]);

    return <RouterProvider router={router} />;
};

export default Router;