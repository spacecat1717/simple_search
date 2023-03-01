#start script

REQUIREMENTS="requirements.txt"
ENV_PATH=.env

install_requirements() {
        pip3 install -r $REQUIREMENTS
}

install_requirements

if [ -f $ENV_PATH ]; then
    echo Database variables already exist

else
    read -p "DB USERNAME = " POSTGRES_USER
    echo "DB_USER=$POSTGRES_USER" >> $ENV_PATH
fi

if grep -q "DB_PASS" $ENV_PATH; then
    echo POSTGRES PASSWORD variable already exists
else
    read -p "DB PASSWORD = " POSTGRES_PASSWORD
    echo "DB_PASSWORD=$POSTGRES_PASSWORD" >> $ENV_PATH
fi

if grep -q "DB_NAME" $ENV_PATH; then
    echo POSTGRES DATABASE variable already exists
else
    read -p "DB DATABASE = " POSTGRES_DB
    echo "DB_NAME=$POSTGRES_DB" >> $ENV_PATH
fi

if grep -q "DB_HOST" $ENV_PATH; then
    echo POSTGRES HOST variable already exists
else
    read -p "DB HOST = " POSTGRES_HOST
    echo "DB_HOST=$POSTGRES_HOST" >> $ENV_PATH
fi

if grep -q "PATH_TO_CSV" $ENV_PATH; then
    echo PATH_TO_CSV variable already exists
else
    read -p "PATH_TO_CSV = " PATH_TO_CSV
    echo "PATH_TO_CSV=$PATH_TO_CSV" >> $ENV_PATH
fi

echo Loading a data from .env file
. $ENV_PATH
echo Loaded

python3.10 main.py