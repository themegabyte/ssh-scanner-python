Small python script to output SSH version and FP to a log file "app.log" in the root dir of the script.

```
git clone git@github.com:themegabyte/ssh-scanner-python.git
cd ssh-scanner-python
python -m venv venv
. ./venv/bin/activate
pip3 install -r requirements.txt
python ./scan.py <HOST> <PORT>

```
