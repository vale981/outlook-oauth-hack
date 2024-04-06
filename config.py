from pathlib import Path
import tomllib
from types import SimpleNamespace
import sys


def get_config(profile):
    with open(Path.home() / ".o365-auth-config.toml", "rb") as f:
       toplevel_data = tomllib.load(f)


    default_data = toplevel_data["default"]
    config_data = default_data | toplevel_data.get(profile, {})
    cache_path = Path.home() / ".cache/o365-oauth" / profile
    cache_path.mkdir(parents=True, exist_ok=True)

    return SimpleNamespace(
        ClientId = config_data["ClientId"],
        ClientSecret = config_data["ClientSecret"],
        Scopes = config_data["Scopes"],
        RefreshTokenFileName = cache_path / "imap_smtp_refresh_token",
        AccessTokenFileName = cache_path / "imap_smtp_access_token",
        Authority = config_data["Authority"] or None,
        Timeout = config_data.get("Timeout", 60 * 60))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(f"Usage: {sys.argv[0]} <profile> <key>")
    print(get_config(sys.argv[1]).__dict__[sys.argv[2]])
