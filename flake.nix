{
  description = "Using OfflineIMAP with M365";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { nixpkgs, flake-utils, mach-nix, ... }:

    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      with pkgs.python3Packages; {
        packages.default = pkgs.stdenv.mkDerivation {
          name = "myscript";
          propagatedBuildInputs = [
            (pkgs.python3.withPackages (pythonPackages: with pythonPackages; [
              msal
            ]))
          ];
          dontUnpack = true;
          installPhase = ''
            install -Dm755 ${./get_token.py} $out/bin/o365-get-token
            install -Dm755 ${./refresh_token.py} $out/bin/o365-refresh-token
            install -Dm755 ${./config.py} $out/bin/config.py
          '';
        };
        homeManagerModules.default = import ./nix/hm-module.nix self;
      });
}
