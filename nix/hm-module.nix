self: {
  config,
  lib,
  pkgs,
  ...
}:
with lib;
let
  inherit (pkgs.stdenv.hostPlatform) system;

  package = self.packages.${system}.default;
  cfg = config.programs.o365-auth;
in {
  options.programs.o365-auth = {
    enable = mkEnableOption "o365 token refresh script";
    config = mkOption {
      type = types.str;
      default = ''
ClientId = "08162f7c-0fd2-4200-a84a-f25a4db0b584"
ClientSecret = "TxRBilcHdC6WGBee]fs?QR:SJ8nI[g82"
Scopes = ['https://outlook.office.com/IMAP.AccessAsUser.All','https://outlook.office.com/SMTP.Send']
RefreshTokenFileName = "imap_smtp_refresh_token"
AccessTokenFileName = "imap_smtp_access_token"

Authority = false
'';
    };
  };
  config = mkIf cfg.enable {
    home.packages = [ package ];
    home.file.".o365-auth-config".source = cfg.config;
  };
}
