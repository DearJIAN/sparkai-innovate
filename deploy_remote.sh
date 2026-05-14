set -e
mkdir -p /data/my-keshe/frontend /data/my-keshe/uploads
cd /data/my-keshe/backend
docker compose down --remove-orphans || true
docker compose up -d --build
docker ps --format '{{.Names}} {{.Ports}}' | grep my-keshe-backend
