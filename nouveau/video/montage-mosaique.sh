#!/usr/bin/env bash
# Vidéo du hero : mosaïque 4×2 des rushes carrés (300×300), 3 compositions
# enchaînées en fondu. Les petites vidéos restent nettes (grossissement ~1,2×).
# Usage : bash video/montage-mosaique.sh
set -euo pipefail
cd "$(dirname "$0")"

SEG=11        # durée de chaque composition (s)
FADE=1        # fondu entre compositions (s)
CW=320; CH=360; GAP=2   # case 320×360 → image 1280×720

# 3 compositions de 8 cases (ordre : ligne du haut, puis ligne du bas)
GRIDS=(
  "deratisation frelons moustiques cafards fourmis pigeons chenilles termites"
  "insectes deratisation taupes moustiques desinfection cafards demoussage fourmis"
  "pigeons frelons termites insectes chenilles taupes deratisation moustiques"
)

inputs=(); filter=""; idx=0; g=0
layout="0_0|w0_0|w0+w1_0|w0+w1+w2_0|0_h0|w0_h0|w0+w1_h0|w0+w1+w2_h0"
for grid in "${GRIDS[@]}"; do
  cells=""; c=0
  for clip in $grid; do
    # départ décalé pour qu'un même clip ne soit jamais identique d'une grille à l'autre
    ss=$(awk -v g="$g" -v c="$c" 'BEGIN{print (g*1.3 + c*0.4) % 2}')
    inputs+=(-stream_loop -1 -ss "$ss" -i "rushes/video_$clip.mp4")
    filter+="[$idx:v]trim=duration=$SEG,setpts=PTS-STARTPTS,fps=25,"
    filter+="scale=$((CH-2*GAP)):$((CH-2*GAP)),crop=$((CW-2*GAP)):$((CH-2*GAP)),"
    filter+="pad=$CW:$CH:$GAP:$GAP:color=0x0b0c0e,setsar=1[c$idx];"
    cells+="[c$idx]"; idx=$((idx+1)); c=$((c+1))
  done
  filter+="${cells}xstack=inputs=8:layout=$layout,format=yuv420p[g$g];"
  g=$((g+1))
done

filter+="[g0][g1]xfade=transition=fade:duration=$FADE:offset=$((SEG-FADE))[x1];"
filter+="[x1][g2]xfade=transition=fade:duration=$FADE:offset=$((2*SEG-2*FADE))[out]"

OUT=../assets/video-hero-rushes
ffmpeg -hide_banner -loglevel error -y "${inputs[@]}" -filter_complex "$filter" -map "[out]" -an \
  -c:v libx264 -preset slow -crf 28 -movflags +faststart "$OUT.mp4"
ffmpeg -hide_banner -loglevel error -y -ss 2 -i "$OUT.mp4" -frames:v 1 -q:v 4 "$OUT-poster.jpg"
ls -lh "$OUT"*
