from pathlib import Path
import tomllib
from types import SimpleNamespace
import sys
import json
import gnupg
gpg = gnupg.GPG()

def get_config(profile):
    with open(Path.home() / ".o365-auth-config.toml", "rb") as f:
       toplevel_data = tomllib.load(f)

    password = None
    if "security" in toplevel_data and "password" in toplevel_data["security"]:
        password = Path(toplevel_data["security"]["PasswordPath"]).read_text().strip()


    default_data = toplevel_data["default"]
    config_data = default_data | toplevel_data.get(profile, {})
    cache_path = Path.home() / ".cache/o365-oauth" / profile
    cache_path.mkdir(parents=True, exist_ok=True)

    return SimpleNamespace(
        ClientId = config_data["ClientId"],
        ClientSecret = config_data["ClientSecret"],
        Scopes = config_data["Scopes"],
        CacheFile = cache_path / "cache.json",
        Authority = config_data["Authority"] or None,
        Password = password
    )

def get_cache(config):
    if not config.CacheFile.exists():
        return None

    data = config.CacheFile.read_text()
    if config.Password:
        data = gpg.decrypt(data, passphrase=config.Password).data.decode("utf-8")

    return json.loads(data)

def write_cache(config, token):
    with open(config.CacheFile, "w") as f:
        payload = {'refresh_token': token['refresh_token'],
               'expires_in': token['expires_in'],
               'access_token': token['access_token']}


        json_string = json.dumps(payload)
        if config.Password:
            encrypted_data = gpg.encrypt(json_string, symmetric="AES256", passphrase=config.Password, armor=True, recipients=None)
            json_string = str(encrypted_data)

        f.write(json_string)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <profile> <key>")
    print(get_config(sys.argv[1]).__dict__[sys.argv[2]])
