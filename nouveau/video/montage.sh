#!/usr/bin/env bash
# Monte la vidéo de couverture à partir des rushes déposés dans video/rushes/.
# Rushes attendus (triés par nom) : 01-rat.mp4, 02-cafard.mp4, … 08-technicien.mp4
# Prérequis : ffmpeg  →  brew install ffmpeg
# Usage : bash video/montage.sh
set -euo pipefail
cd "$(dirname "$0")"

# Durée gardée pour chaque plan (s) et point d'entrée dans le rush (s)
DUR=(4.2 4.2 4.2 4.2 4.2 4.2 4.2 5.0)
START=(1 1 1 1 1 1 1 1)
FADE=0.5                     # fondu enchaîné entre deux plans
W=1280; H=720; FPS=30        # 720p suffit pour un fond de hero

shopt -s nullglob
CLIPS=(rushes/*.mp4 rushes/*.mov)
IFS=$'\n' CLIPS=($(printf '%s\n' "${CLIPS[@]}" | sort)); unset IFS
N=${#CLIPS[@]}
if (( N < 2 )); then echo "Déposez au moins 2 rushes dans video/rushes/"; exit 1; fi
(( N > ${#DUR[@]} )) && N=${#DUR[@]}

inputs=(); filter=""
for ((k=0; k<N; k++)); do
  inputs+=(-i "${CLIPS[k]}")
  filter+="[$k:v]trim=start=${START[k]}:duration=${DUR[k]},setpts=PTS-STARTPTS,"
  filter+="scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,fps=$FPS,format=yuv420p[v$k];"
done

prev="v0"; acc=0
for ((k=1; k<N; k++)); do
  acc=$(awk -v a="$acc" -v d="${DUR[k-1]}" 'BEGIN{print a+d}')
  offset=$(awk -v a="$acc" -v k="$k" -v f="$FADE" 'BEGIN{print a-k*f}')
  out="x$k"; (( k == N-1 )) && out="out"
  filter+="[$prev][v$k]xfade=transition=fade:duration=$FADE:offset=$offset[$out];"
  prev="$out"
done
filter="${filter%;}"

OUT=../assets/video-eden-originale
ffmpeg -y "${inputs[@]}" -filter_complex "$filter" -map "[out]" -an \
  -c:v libx264 -preset slow -crf 28 -movflags +faststart "$OUT.mp4"
ffmpeg -y -i "$OUT.mp4" -an -c:v libvpx-vp9 -crf 38 -b:v 0 "$OUT.webm"
ffmpeg -y -ss 1 -i "$OUT.mp4" -frames:v 1 -q:v 3 "$OUT-poster.jpg"

ls -lh "$OUT".*
