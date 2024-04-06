#! /usr/bin/env python3
from msal import ConfidentialClientApplication, SerializableTokenCache
import config
import sys
import os
import time
import json
print_access_token = True

if len(sys.argv) > 1:
    profile = sys.argv[1]
else:
    sys.exit("Please provide a profile name as the first argument.")


profile_config = config.get_config(profile)
# We use the cache to extract the refresh token
cache = SerializableTokenCache()
app = ConfidentialClientApplication(profile_config.ClientId, client_credential=profile_config.ClientSecret, token_cache=cache, authority=profile_config.Authority)


if not profile_config.CacheFile.exists():
    sys.exit("Please get the initial token by running `o365-get-token` first.")

token_cache = json.loads(profile_config.CacheFile.read_text())

st = os.stat(profile_config.CacheFile)
if (time.time()-st.st_mtime) < token_cache["expires_in"]:
    print(token_cache["access_token"])
    sys.exit(0)


token = app.acquire_token_by_refresh_token(token_cache["refresh_token"],profile_config.Scopes)

if 'error' in token:
    print(token)
    sys.exit("Failed to get access token")


# you're supposed to save the old refresh token each time
with open(profile_config.CacheFile, 'w') as f:
    json.dump({'refresh_token': token['refresh_token'],
               'expires_in': token['expires_in'],
               'access_token': token['access_token']}, f)
    if print_access_token:
        print(token['access_token'])
