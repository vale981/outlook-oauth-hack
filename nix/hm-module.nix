self: { config
      , lib
      , pkgs
      , ...
      }:
with lib;
let
  inherit (pkgs.stdenv.hostPlatform) system;

  package = self.packages.${system}.default;
  cfg = config.programs.o365-auth;
in
{
  options.programs.o365-auth = {
    enable = mkEnableOption "o365 token refresh script";
    package = mkOption {
      type = types.package;
      default = package;
    };
    config = mkOption {
      type = types.str;
      default = ''
        [default]
        ClientId = "08162f7c-0fd2-4200-a84a-f25a4db0b584"
        ClientSecret = "TxRBilcHdC6WGBee]fs?QR:SJ8nI[g82"
        Scopes = ['https://outlook.office.com/IMAP.AccessAsUser.All','https://outlook.office.com/SMTP.Send']
        Authority = false
      '';
    };
  };
  config = mkIf cfg.enable {
    home.packages = [ cfg.package ];
    home.file.".o365-auth-config".text = cfg.config;
  };
}
