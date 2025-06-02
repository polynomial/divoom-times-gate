{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    python311Packages.setuptools
    python311Packages.wheel
    python311Packages.aiohttp
    python311Packages.requests
  ];

  shellHook = ''
    echo "Divoom Times Gate Development Environment"
    echo "Python: $(python --version)"
    echo ""
    echo "To install the package in development mode:"
    echo "  pip install -e ."
    echo ""
    echo "To install dependencies only:"
    echo "  pip install -r requirements.txt"
    echo ""
    echo "To run tests:"
    echo "  python -m pytest tests/"
    echo ""
    export PYTHONPATH="$PWD:$PYTHONPATH"
  '';
}
