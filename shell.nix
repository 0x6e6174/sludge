{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python312
    pkgs.python312Packages.networkx
    pkgs.python312Packages.matplotlib
    pkgs.python312Packages.requests
    pkgs.python312Packages.bleach
    pkgs.python312Packages.beautifulsoup4
    pkgs.python312Packages.pygraphviz
    pkgs.python312Packages.requests_toolbelt
  ];
  shellHook = ''
    python src/main.py
  '';
}
