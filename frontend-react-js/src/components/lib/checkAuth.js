import { fetchUserAttributes } from "aws-amplify/auth";


const checkAuth = async (setUser) => {
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

export default checkAuth;