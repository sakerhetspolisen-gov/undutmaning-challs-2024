#!/bin/bash
# entrypoint.sh

# Start the web terminal server in the background
node /home/ctf/app/web-terminal-server.js &
#
set -eu
tmux attach
#
exec "$@"

