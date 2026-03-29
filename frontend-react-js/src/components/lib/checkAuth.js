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
        const attributes = await fetchUserAttributes();

        setUser({
            display_name: attributes.name,
            handle: attributes.preferred_username,
        });
    } catch (err) {
        console.log(err);
    }
};
