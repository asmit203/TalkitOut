# TalkitOut
Complete Blogging Website created using React and Django

## USAGE
```bash
git clone https://github.com/asmit203/TalkitOut.git
cd TalkitOut
```
the install all the dependencies using
```bash
pip install -r requirements.txt
```
then run the server using
```bash
cd "TalkitOut-Backend (REST-APIs)"
python manage.py runserver 8000
```
start frontend react server (in a new terminal) using
```bash
cd talkitout-frontend
npm start
```
this will automatically open localhost:3000 in your default browser

**Also Whenever Cloning This Repo Please Delete all `migration` and `pycache `files**

### Don't Forget to add a db.sqlite3 for the database to run

#### for forceful creation of tables `python manage.py migrate --run-syncdb `
