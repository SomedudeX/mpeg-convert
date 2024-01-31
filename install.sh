echo " - Receiving dependencies for mpeg-convert"
curl -s https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/v1.0.0/requirements.txt > requirements.txt

echo " - Installing dependencies with pip3: \n   * python-ffmpeg\n   * rich"
python -m pip install -r requirements.txt

echo " - Receiving script for mpeg-convert"
curl -s https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/main/App/mpeg-convert.py > mpeg-convert.py
echo " - Received mpeg-convert.py"

echo " - Purging files"
rm requirements.txt

echo " - Notes: \n       You may want to 'sudo chmod +x' the file"
echo " - Installation script finished"
