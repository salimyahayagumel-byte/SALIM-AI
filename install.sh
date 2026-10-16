#!/data/data/com.termux/files/usr/bin/bash
set -e
cd "$(dirname "$0")"
pkg update -y
pkg install -y python
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if [ ! -f .env ]; then cp .env.example .env; fi
echo
echo "An gama girka SALIM AI."
echo "Ka buɗe .env ka saka GROQ_API_KEY, sannan ka kunna: bash run.sh"
