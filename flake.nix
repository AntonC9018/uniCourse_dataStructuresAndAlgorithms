{
  description = "Pinned toolchain for the course's compiler-backed visualizations";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forEachSystem = f: nixpkgs.lib.genAttrs systems
        (system: f nixpkgs.legacyPackages.${system});
    in {
      devShells = forEachSystem (pkgs: rec {
        # What CI enters to trace tagged examples with the `visualizations` submodule.
        # Its lock is part of every trace key.
        visualizations = pkgs.mkShellNoCC {
          packages = [ pkgs.clang pkgs.gdb pkgs.python3 ];
          CLANGXX = "${pkgs.clang}/bin/clang++";
          GDB = "${pkgs.gdb}/bin/gdb";
        };
        # Local player work: the tracer plus the browser used for screenshots.
        default = pkgs.mkShellNoCC {
          inputsFrom = [ visualizations ];
          inherit (visualizations) CLANGXX GDB;
          packages = [ pkgs.nodejs_22 pkgs.chromium ];
          CHROMIUM_EXECUTABLE = "${pkgs.chromium}/bin/chromium";
        };
      });
    };
}
