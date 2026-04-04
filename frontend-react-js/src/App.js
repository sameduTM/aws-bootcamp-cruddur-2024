/* eslint-disable */
import "./App.css";

import HomeFeedPage from "./pages/HomeFeedPage";
import NotificationsFeedPage from "./pages/NotificationsFeedPage";
import UserFeedPage from "./pages/UserFeedPage";
import SignupPage from "./pages/SignupPage";
import SigninPage from "./pages/SigninPage";
import RecoverPage from "./pages/RecoverPage";
import MessageGroupsPage from "./pages/MessageGroupsPage";
import MessageGroupPage from "./pages/MessageGroupPage";
import MessageGroupNewPage from "./pages/MessageGroupNewPage";
import ConfirmationPage from "./pages/ConfirmationPage";
import React from "react";
import process from "process";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { Amplify } from 'aws-amplify';


Amplify.configure({
  Auth: {
    Cognito: {
      region: process.env.REACT_APP_AWS_PROJECT_REGION,
      userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,
      userPoolClientId: process.env.REACT_APP_CLIENT_ID,
      oauth: {}
    }
  }
});

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomeFeedPage />,
  },
  {
    path: "/notifications",
    element: <NotificationsFeedPage />,
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />,
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />,
  },
  {
    path: "/messages/:message_group_uuid",
    element: <MessageGroupPage />,
  },
  {
    path: "/messages/new/:handle",
    element: <MessageGroupNewPage />,
  },
  {
    path: "/signup",
    element: <SignupPage />,
  },
  {
    path: "/signin",
    element: <SigninPage />,
  },
  {
    path: "/confirm",
    element: <ConfirmationPage />,
  },
  {
    path: "/forgot",
    element: <RecoverPage />,
  },
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;
