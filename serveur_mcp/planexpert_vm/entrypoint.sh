#!/bin/sh
# ~/.ssh monté en lecture seule (droits Windows/WSL permissifs) -> ssh le refuse tel quel
# ("Bad owner or permissions"). On copie dans un ~/.ssh writable du conteneur, droits corrects.
set -e
if [ -d /root/.ssh-src ]; then
    mkdir -p /root/.ssh
    cp -r /root/.ssh-src/. /root/.ssh/
    chmod 700 /root/.ssh
    find /root/.ssh -type f -exec chmod 600 {} \;
fi
exec python /app/server.py "$@"
