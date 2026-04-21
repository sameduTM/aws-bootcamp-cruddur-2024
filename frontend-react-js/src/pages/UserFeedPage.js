import './UserFeedPage.css';
import React from "react";
import { useParams } from 'react-router-dom';

import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';

// Authentication
import { checkAuth, getAccessToken } from '../components/lib/checkAuth';
import ProfileHeading from '../components/ProfileHeading';
import ProfileForm from '../components/ProfileForm';

export default function UserFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [profile, setProfile] = React.useState([]);
  const [popped, setPopped] = React.useState([]);
  const [poppedProfile, setPoppedProfile] = React.useState([]);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const params = useParams();

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/@${params.handle}`;
      const access_token = await getAccessToken();
      const res = await fetch(backend_url, {
        method: "GET",
        headers: {
          'Authorization': `Bearer ${access_token}`
        }

      });
      let resJson = await res.json();
      if (res.status === 200) {
        setProfile(resJson.profile);
        setActivities(resJson.activities);
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };

  React.useEffect(() => {
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    // const loadData = async () => {
    //   // your function logic here
    // };
    loadData();
    checkAuth(setUser);
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'profile'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm popped={popped} setActivities={setActivities} />
        <ProfileForm
          profile={profile}
          popped={poppedProfile}
          setPopped={setPoppedProfile}
        />
        <div className='activity_feed'>
          <ProfileHeading setPopped={setPoppedProfile} profile={profile}></ProfileHeading>
          <ActivityFeed activities={activities} />
        </div>
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}