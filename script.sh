pip3 install virtualenv &&

virtualenv env &&
source env/bin/activate &&
pip3 install -r requirements.txt &&

python3 manage.py makemigrations &&
python3 manage.py migrate
