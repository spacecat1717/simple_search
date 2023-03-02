REQUIREMENTS="requirements.txt"

install_requirements() {
        pip3 install -r $REQUIREMENTS
}
echo Installing requirements...
install_requirements

echo Done.

echo Preparing service to start...
python3.10 pre_run.py
echo Done. Now you can use start.sh script