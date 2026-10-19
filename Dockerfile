# Serveur MCP « Expert estimateur » — un seul serveur pour tous les collègues (même PDF = même résultat).
# docker build -t expert-estimateur . && docker run -p 8765:8765 -v estim:/data \
#   -e ESTIMATEUR_MCP_CLE=<clé> -e ESTIMATEUR_URL_PUBLIQUE=https://<hôte> -e ESTIMATEUR_HOTE_PERMIS=<hôte> expert-estimateur
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# /data : dossiers de travail + bibliothèque de blocs apprise (survit aux redéploiements)
ENV ESTIMATEUR_BASE=/data/dossiers ESTIMATEUR_BIBLIOTHEQUE=/data/bibliotheque-blocs.csv PYTHONUTF8=1
VOLUME /data
EXPOSE 8765
CMD ["sh", "-c", "mkdir -p /data/dossiers && ([ -f /data/bibliotheque-blocs.csv ] || cp releve/bibliotheque-blocs.csv /data/) && exec python -m serveur_mcp --transport http --hote 0.0.0.0 --port 8765 --hote-permis \"${ESTIMATEUR_HOTE_PERMIS:-localhost}\""]
