#! /usr/bin/env python3
from msal import ConfidentialClientApplication, SerializableTokenCache
import config
import sys


print_access_token = True
# get first command line argument

if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    sys.exit("Please provide a profile name as the first argument.")


profile_config = config.get_config(profile)
# We use the cache to extract the refresh token
cache = SerializableTokenCache()
app = ConfidentialClientApplication(profile_config.ClientId, client_credential=profile_config.ClientSecret, token_cache=cache, authority=profile_config.Authority)


# check if file exists and error out if it doesn't
try:
    old_refresh_token = open(profile_config.RefreshTokenFileName,'r').read()
except FileNotFoundError:
    sys.exit("Please get the initial token by running `o365-get-token` first.")


token = app.acquire_token_by_refresh_token(old_refresh_token,profile_config.Scopes)

if 'error' in token:
    print(token)
    sys.exit("Failed to get access token")

# you're supposed to save the old refresh token each time
with open(profile_config.RefreshTokenFileName, 'w') as f:
    #f.write(cache.find('RefreshToken')[0]['secret'])
    f.write(token['refresh_token'])

with open(profile_config.AccessTokenFileName, 'w') as f:
    f.write(token['access_token'])
    if print_access_token:
        print(token['access_token'])
