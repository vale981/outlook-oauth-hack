from pathlib import Path
import tomllib

with open(Path.home() / ".o365-oauth-config.toml", "rb") as f:
    config_data = tomllib.load(f)

cache_path = Path.home() / ".chache/o365-oauth"
cache_path.mkdir(parents=True, exist_ok=True)

ClientId = config_data["ClientId"]
ClientSecret = config_data["ClientSecret"]
Scopes = config_data["Scopes"]
RefreshTokenFileName = cache_path / "imap_smtp_refresh_token"
AccessTokenFileName = cache_path / "imap_smtp_access_token"

Authority = config_data["Authority"] or None
