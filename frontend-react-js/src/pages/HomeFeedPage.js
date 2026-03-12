import "./HomeFeedPage.css";
import React from "react";

import DesktopNavigation from "../components/DesktopNavigation";
import DesktopSidebar from "../components/DesktopSidebar";
import ActivityFeed from "../components/ActivityFeed";
import ActivityForm from "../components/ActivityForm";
import ReplyForm from "../components/ReplyForm";

// [TODO] Authenication
import { fetchUserAttributes, fetchAuthSession } from "aws-amplify/auth";

export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`;
      const session = await fetchAuthSession();
      const accessToken = session.tokens?.accessToken?.toString();
      
      const user_handle = session.tokens.idToken.payload.preferred_username

      const res = await fetch(backend_url, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Username: user_handle,
        },
      });

      let resJson = await res.json();

      if (res.status === 200) {
        setActivities(resJson);
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  };

  // check if we are authenicated

  const checkAuth = async () => {
    try {
      const attributes = await fetchUserAttributes();

      setUser({
        display_name: attributes.name,
        handle: attributes.preferred_username,
      });
    } catch (err) {
      console.log(err);
    }
  };

  // check when the page loads if we are authenicated
  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth();
  }, []);

  return (
    <article>
      <DesktopNavigation user={user} active={"home"} setPopped={setPopped} />
      <div className="content">
        <ActivityForm
          popped={popped}
          setPopped={setPopped}
          setActivities={setActivities}
        />
        <ReplyForm
          activity={replyActivity}
          popped={poppedReply}
          setPopped={setPoppedReply}
          setActivities={setActivities}
          activities={activities}
        />
        <ActivityFeed
          title="Home"
          setReplyActivity={setReplyActivity}
          setPopped={setPoppedReply}
          activities={activities}
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
