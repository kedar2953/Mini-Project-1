
from distutils.log import debug
from app import create_app

create_app().run(host="127.0.0.1", port=5000,debug=True)
