echo "Receiving dependencies for mpeg-convert"
curl -s https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/v1.0.0/requirements.txt > requirements.txt

echo "Installing dependencies with pip3: \n - python-ffmpeg\n - rich"
pip3 install -r requirements.txt

echo "Receiving script for mpeg-convert"
curl -s https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/v1.1.0/App/mpeg-convert.py > mpeg-convert.py

rm requirements.txt

echo "Succesfully installed mpeg-convert.py"
echo "You may want to chmod +x the file"
