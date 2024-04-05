from pathlib import Path
import tomllib
from types import SimpleNamespace
import sys


def get_config(profile):
    with open(Path.home() / ".o365-auth-config.toml", "rb") as f:
       toplevel_data = tomllib.load(f)

    if profile not in toplevel_data:
        sys.exit("Invalid profile specified.")

    config_data = toplevel_data[profile]
    cache_path = Path.home() / ".cache/o365-oauth" / profile
    cache_path.mkdir(parents=True, exist_ok=True)

    return SimpleNamespace(
        ClientId = config_data["ClientId"],
        ClientSecret = config_data["ClientSecret"],
        Scopes = config_data["Scopes"],
        RefreshTokenFileName = cache_path / "imap_smtp_refresh_token",
        AccessTokenFileName = cache_path / "imap_smtp_access_token",
        Authority = config_data["Authority"] or None)
