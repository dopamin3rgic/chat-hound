#!/usr/bin/bash
echo "navigating to repository root"
cd .. 

echo "creating virtual environment..."
python3 -m venv env

echo "activating virtual environment"
source ./env/bin/activate

echo "installing requirements"
pip install -r ./dev/requirements.txt