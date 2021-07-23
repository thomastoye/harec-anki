{ nixpkgs ? import (fetchTarball https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz) {} }:
with nixpkgs;

let
  customPython = python39.buildEnv.override {
    extraLibs = [
      python39Packages.genanki
    ];
  };
in
  pkgs.mkShell {
    buildInputs = [
      customPython
    ];
  }
