from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

class CustomAccessToken(AccessToken):
    
    @classmethod
    def from_user(cls, user):
        token = cls()
        
        # adding claims to the token
        token['user_id'] = str(user.pk)
        token['username'] = user.get_username()
        
        # adding the custom fields
        token['name'] = user.name
        token['user_type'] = user.user_type
        token['is_moderator'] = user.is_moderator
        token['last_verified_identity'] = user.last_verified_identity
        
        return token


class Authenctication:
    def get_access_token_from_refresh(refresh_token):
        pass
    
    def get_access_token(self, user):
        return CustomAccessToken.from_user(user)
        
    def get_tokens_for_user(self, user):
        refresh_token = RefreshToken.for_user(user)
        access_token = self.get_access_token(user)
        
        return access_token, refresh_token