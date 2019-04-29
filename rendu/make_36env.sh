# wget https://bootstrap.pypa.io/get-pip.py
# sudo python3.6 get-pip.py
python3.6 -m pip -V

sudo python3.6 -m pip install virtualenv
python3.6 -m virtualenv pyjupy36
source pyjupy36/bin/activate
python --version

pip install ipykernel
pip install keras
pip install tensorflow
pip install pandas



# python3.6 --version