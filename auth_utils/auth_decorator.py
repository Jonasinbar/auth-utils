import jwt
import os

LOGIN_MANAGER_ADDRESS = 'loginmanager:50051'


def jwt_authentication_required(return_user=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            context = args[2]
            metadata = dict(context.invocation_metadata())
            token = metadata.get('authorization')

            if not token:
                return func(*args, success=False, auth_result="Token is missing", **kwargs)

            try:
                # Read the public key from the environment variable
                public_key = os.getenv('PUBLIC_KEY')
                if not public_key:
                    raise ValueError("Environment variable 'PUBLIC_KEY' not set")

                # Decode and verify the token using the public key
                decoded_token = jwt.decode(token, public_key, algorithms=['RS256'])
                user_id = decoded_token
                if return_user:
                    return func(*args, success=True, auth_result=user_id, **kwargs)
                else:
                    return func(*args, success=True, auth_result=None, **kwargs)

            except jwt.ExpiredSignatureError:
                return func(*args, success=False, auth_result="Token has expired", **kwargs)
            except jwt.InvalidTokenError:
                return func(*args, success=False, auth_result="Invalid token", **kwargs)

        return wrapper
    return decorator
