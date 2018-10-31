with import <nixpkgs> {};
stdenv.mkDerivation rec {
  name = "env";
  env = buildEnv { name = name; paths = buildInputs; };
  buildInputs = [
    python
    python27Packages.beautifulsoup4
    python27Packages.requests
  ];
}

