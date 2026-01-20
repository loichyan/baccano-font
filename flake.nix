{
  inputs = {
    nixpkgs.url = "nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        inherit (pkgs) mkShellNoCC;
        python3 = pkgs.python312.withPackages (ps: [ ps.fontforge ]);
      in
      {
        devShells.default = mkShellNoCC {
          packages = with pkgs; [
            python3
            uv
            ty
            ruff
          ];
        };
      }
    );
}
