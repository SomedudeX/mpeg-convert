echo " - Checking the installation of curl"
if ! command -v curl >/dev/null 2>&1; then
    echo " - Error: curl is not installed"
    echo "   > Make sure to install curl"
    echo "   > Script cannot proceed"
    exit 1
fi; 

echo " - Checking the installation of Python 3"
if ! command -v python3 >/dev/null 2>&1; then
    echo " - Error: Python is not installed"
    echo "   > Make sure to install Python 3"
    echo "   > Script cannot proceed"
    exit 1
fi;


echo " - Checking the installation of FFmpeg"
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo " - Warning: FFmpeg is not installed"
    echo "   > Mpeg-convert.py requires FFmpeg to be installed on your system"
    echo "   > Make sure to install it as soon as possible! "
fi;

echo " - Receiving dependency list for mpeg-convert (requirements.txt)"
curl -s https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/v1.0.0/requirements.txt > requirements.txt
echo " - Received requirements.txt"

echo " - Receiving script (mpeg-convert.py)"
curl -s https://raw.githubusercontent.com/SomedudeX/MPEG-Convert/main/App/mpeg-convert.py > mpeg-convert.py
echo " - Received mpeg-convert.py"

echo " - Installing dependencies with pip3: \n   * python-ffmpeg\n   * rich"
python -m pip install -r requirements.txt >/dev/null 2>&1

echo " - Cleaning up"
rm requirements.txt

echo " - Installation script finished"
echo " - Notes: \n       You may want to 'sudo chmod +x' the file"

echo "       Script located in $(eval pwd)/mpeg-convert.py\n"


