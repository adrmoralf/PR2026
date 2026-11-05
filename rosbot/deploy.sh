#!/usr/bin/env bash
# Sincroniza esta carpeta con el ROSbot y reinicia solo lo que haya cambiado.
#
# Uso:
#   ./deploy.sh              sincroniza y aplica los cambios
#   ./deploy.sh --dry-run    muestra qué se copiaría, sin tocar el robot
#   ./deploy.sh --sync-only  copia los ficheros pero no reinicia nada
#   ./deploy.sh --pull-map   descarga el mapa del robot a ./maps
#
# Variables:
#   ROBOT=husarion@172.20.10.8   destino SSH (cambiar si cambia la IP)
#   REMOTE_DIR=rosbot-autonomy   carpeta en el home del robot
set -euo pipefail

ROBOT="${ROBOT:-husarion@172.20.10.8}"
REMOTE_DIR="${REMOTE_DIR:-rosbot-autonomy}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-deploy}"

RSYNC_OPTS=(-rlpz --checksum --delete --itemize-changes
  --exclude='.git/' --exclude='maps/' --exclude='.vscode/' --exclude='deploy.sh'
  --exclude='sim/' --exclude='__pycache__/' --exclude='test/')

case "$MODE" in
  --pull-map)
    mkdir -p "$HERE/maps"
    rsync -av "$ROBOT:$REMOTE_DIR/maps/" "$HERE/maps/"
    exit 0 ;;
  --dry-run)
    rsync "${RSYNC_OPTS[@]}" --dry-run "$HERE/" "$ROBOT:$REMOTE_DIR/"
    exit 0 ;;
  deploy|--sync-only) ;;
  *) sed -n 2,12p "$0"; exit 1 ;;
esac

# Valida el Compose en local antes de copiar nada (si hay docker en el PC).
if command -v docker >/dev/null 2>&1; then
  (cd "$HERE" && docker compose config --quiet)
fi

echo ">> Sincronizando $HERE -> $ROBOT:$REMOTE_DIR"
CHANGES="$(rsync "${RSYNC_OPTS[@]}" "$HERE/" "$ROBOT:$REMOTE_DIR/" | grep -vE '^\.d' || true)"
if [[ -z "$CHANGES" ]]; then
  echo ">> Sin cambios."
  exit 0
fi
echo "$CHANGES"

[[ "$MODE" == "--sync-only" ]] && exit 0

# Los ficheros montados como volumen (config/, filter.yaml) no provocan que
# 'docker compose up' recree el contenedor, así que se reinicia a mano.
RESTART=()
grep -qE ' config/nav2_' <<<"$CHANGES" && RESTART+=(navigation)
grep -qE ' filter\.yaml' <<<"$CHANGES" && RESTART+=(ros2router)
# El código del camarero se monta como volumen: reiniciar si está activo.
grep -qE ' camarero/' <<<"$CHANGES" && RESTART+=(camarero)

ssh "$ROBOT" bash -s -- "$REMOTE_DIR" "${RESTART[@]}" <<'EOF'
set -euo pipefail
cd "$HOME/$1"; shift
docker compose config --quiet
# Recrea los servicios cuyo compose.yaml o .env haya cambiado.
docker compose up -d --remove-orphans
# Reinicia solo los servicios pedidos que estén en marcha (camarero puede estar desactivado).
ACTIVOS=" $(docker compose ps --services --status running | tr '\n' ' ') "
PEDIDOS=()
for s in "$@"; do [[ "$ACTIVOS" == *" $s "* ]] && PEDIDOS+=("$s"); done
if [[ ${#PEDIDOS[@]} -gt 0 ]]; then
  echo ">> Reiniciando: ${PEDIDOS[*]}"
  docker compose restart "${PEDIDOS[@]}"
fi
docker compose ps
EOF
