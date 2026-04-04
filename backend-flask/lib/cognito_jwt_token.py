import cognitojwt
import os

REGION = os.getenv("AWS_DEFAULT_REGION")
USERPOOL_ID = os.getenv("AWS_COGNITO_USER_POOL_ID")
APP_CLIENT_ID = os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID")


class TokenVerify:    
    def cognito_jwt_verify(id_token: str):
        verified_claims: dict = cognitojwt.decode(
            id_token.removeprefix('Bearer '),
            REGION,
            USERPOOL_ID,
            app_client_id=APP_CLIENT_ID,  # Optional
            # testmode=True  # Disable token expiration check for testing purposes
        )

        return verified_claims
