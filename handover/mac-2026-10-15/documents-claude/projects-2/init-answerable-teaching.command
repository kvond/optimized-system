#!/bin/bash
# One-time setup for the Answerable Teaching book repo.
# Run this ONCE. After it succeeds, never run it again (it wipes and re-clones).
# For day-to-day pushes, see the note at the bottom.
set -e

REPO=~/Documents/Answerable-Teaching

echo "Setting up $REPO ..."
rm -rf "$REPO"
git clone https://github.com/kvond/Answerable-Teaching.git "$REPO"
cd "$REPO"
echo "# Answerable Teaching" > README.md
git add README.md
git commit -m "Initialize repo"
git push

echo ""
echo "✅ Done — README.md committed and pushed to GitHub."

# ---------------------------------------------------------------------------
# AFTER THIS: you do NOT re-run this script. To push future changes, just do,
# from inside ~/Documents/Answerable-Teaching :
#     git add -A
#     git commit -m "what changed"
#     git push
# ---------------------------------------------------------------------------
