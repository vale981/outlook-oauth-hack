{
  description = "Using OfflineIMAP with M365";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    systems.url = "github:nix-systems/default";
  };
  outputs = { self, nixpkgs, flake-utils, systems, ... }:
    let
      eachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      homeManagerModules.default = import ./nix/hm-module.nix self;


      packages = eachSystem (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        with pkgs.python3Packages; {
          default = pkgs.stdenv.mkDerivation {
            name = "o365-auth";
            propagatedBuildInputs = [
              (pkgs.python3.withPackages (pythonPackages: with pythonPackages; [
                msal python-gnupg
              ]))
            ];
            dontUnpack = true;
            installPhase = ''
              install -Dm755 ${./get_token.py} $out/bin/o365-get-token
              install -Dm755 ${./refresh_token.py} $out/bin/o365-refresh-token
              install -Dm755 ${./config.py} $out/bin/config.py
              install -Dm755 ${./config.py} $out/bin/o365-get-config
            '';
          };
        });
    };
}
