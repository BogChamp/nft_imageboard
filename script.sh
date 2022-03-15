pip3 install virtualenv &&

virtualenv env &&
source env/bin/activate &&
pip3 install django &&
pip3 install pillow &&
pip3 install imagehash &&

python3 manage.py makemigrations &&
python3 manage.py migrate
