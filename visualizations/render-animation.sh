#!/usr/bin/env bash
# Run from the course root, inside the maintenance toolchain environment.
set -euo pipefail
visualization_python="${VISUALIZATION_PYTHON:-course_maintenance/.venv/bin/python}"
export PYTHONPATH="$PWD/visualizations${PYTHONPATH:+:$PYTHONPATH}"
"$visualization_python" visualizations/render.py
"$visualization_python" -m manim --disable_caching --media_dir visualizations/media \
  visualizations/scenes.py ExpressionTimeline SwapTimeline
cp visualizations/media/videos/scenes/720p24/ExpressionTimeline.mp4 \
  visualizations/renders/expression.mp4
cp visualizations/media/videos/scenes/720p24/SwapTimeline.mp4 \
  visualizations/renders/swap.mp4
"$visualization_python" visualizations/review.py
