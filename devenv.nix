{ pkgs, ... }:

{
  # https://devenv.sh/packages/
  packages = [ 
    pkgs.git
    pkgs.python310Packages.pip
    pkgs.python310Packages.pillow
    pkgs.python310Packages.piexif
    pkgs.python310Packages.pytest
  ];

  enterShell = ''
    python --version
  '';

  # https://devenv.sh/languages/
  languages.python.enable = true;

  # https://devenv.sh/pre-commit-hooks/
  pre-commit.hooks = {
    # lint shell scripts
    shellcheck.enable = true;

    # format Python code
    black.enable = true;
  };
}
