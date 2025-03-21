let
  pkgs = import <nixpkgs> {};

in
  pkgs.mkShell {
    buildInputs = with pkgs; [
      less
      vim
      jq.bin
      vim
      python310Full
      poetry
      #openai
    ];

    shellHook = ''
      export AI_HOME=${builtins.getEnv "PWD"}
      export PYTHONPATH=${builtins.getEnv "PWD"}:$PYTHONPATH
      export PYTHON_LD_LIBRARY_PATH=${builtins.getEnv "PWD"}/src:${pkgs.lib.makeLibraryPath [
        # Needed for pandas / numpy
        pkgs.stdenv.cc.cc.lib
        pkgs.zlib
        # Needed for pygame
        pkgs.glib
        # Needed for matplotlib
        pkgs.xorg.libX11
      ]}
      export LD_LIBRARY_PATH=$PYTHON_LD_LIBRARY_PATH 
      export PYTHONHOME=${pkgs.python310Full}
      export PYTHONBIN=${pkgs.python310Full}/bin/python3.10
      export LANG=en_US.UTF-8
    '';
  }
