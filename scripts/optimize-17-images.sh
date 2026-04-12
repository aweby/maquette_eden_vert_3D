#!/usr/bin/env bash
# Génère les variantes utilisées par 17.html (logo + cartes urgence).
# Prérequis : macOS (sips). Placez les fichiers sources à la racine du site :
#   logo.png, images/deratisation.jpg, images/cafards.jpg, …
# Usage : depuis la racine du projet : bash scripts/optimize-17-images.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v sips >/dev/null 2>&1; then
  echo "sips est introuvable (macOS requis)." >&2
  exit 1
fi

resize_jpeg() {
  local src=$1 max_side=$2 dst=$3 quality=$4
  [[ -f "$src" ]] || { echo "Absent : $src" >&2; return 1; }
  sips -Z "$max_side" -s format jpeg -s formatOptions "$quality" "$src" --out "$dst" >/dev/null
  echo "OK $dst"
}

resize_png() {
  local src=$1 max_side=$2 dst=$3
  [[ -f "$src" ]] || { echo "Absent : $src" >&2; return 1; }
  sips -Z "$max_side" -s format png "$src" --out "$dst" >/dev/null
  echo "OK $dst"
}

if [[ -f logo.png ]]; then
  resize_png logo.png 400 logo-400w.png
  resize_png logo.png 800 logo-800w.png
else
  echo "Absent : logo.png (ignoré)"
fi

JPEGS=(
  deratisation cafards punaises frelons moustiques fourmis pigeons taupes desinfection
)

for base in "${JPEGS[@]}"; do
  src="images/${base}.jpg"
  [[ -f "$src" ]] || { echo "Absent : $src (ignoré)"; continue; }
  resize_jpeg "$src" 480 "images/${base}-480w.jpg" 78
  resize_jpeg "$src" 720 "images/${base}-720w.jpg" 80
done

echo "Terminé. Déployez logo-400w.png, logo-800w.png et les fichiers *-480w.jpg / *-720w.jpg avec 17.html."
