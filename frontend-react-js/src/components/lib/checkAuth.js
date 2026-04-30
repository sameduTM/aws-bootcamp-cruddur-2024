import { fetchAuthSession, fetchUserAttributes } from "aws-amplify/auth";

export const getAccessToken = async () => {
    try {
        const session = await fetchAuthSession();
        const access_token = session.tokens.accessToken.toString();
        return access_token;
    } catch (err) {
        console.log('getAccessTokenError:', err);
    }

}

export const checkAuth = async (setUser) => {
    try {
        const { sub, name, preferred_username } = await fetchUserAttributes();
        setUser({
            cognito_user_uuid: sub,
            display_name: name,
            handle: preferred_username,
        });
    } catch (err) {
        console.log(err);
    }
};
