# syntax=docker/dockerfile:1
FROM python:3.12-slim

# openssh-client : le serveur pilote mxlinux/la VM Windows exclusivement par ssh/scp
# (voir server.py : sh(["ssh", ... "mx"/"winsrv" ...])). rsync utile pour download().
RUN apt-get update \
    && apt-get install -y --no-install-recommends openssh-client rsync ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Dépendances du script (déclarées en en-tête PEP 723 de server.py)
RUN pip install --no-cache-dir "mcp==2.2.0" "pillow>=10"

WORKDIR /app
COPY server.py /app/server.py

# Dossier des captures : surchargé par PLANEXPERT_VM_SHOTS (chemin Windows par défaut
# dans server.py, non valide en conteneur) -> on force un chemin conteneur ici.
ENV PLANEXPERT_VM_SHOTS=/data/captures
RUN mkdir -p /data/captures

# Clés/host connus SSH montées en lecture seule par docker-compose (~/.ssh hôte -> /root/.ssh-src)
# Config attendue : hôtes "mx" (root@mxlinux) et "winsrv" (francis@VM:2222), voir README.md.
# entrypoint.sh les recopie dans /root/.ssh (writable) avec les bons droits (ssh refuse un
# ~/.ssh monté RO aux permissions Windows/WSL : "Bad owner or permissions").
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
