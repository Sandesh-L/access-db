#ASSUMING setup.sh is already run

DB_DIR=postgres_db
DB_NAME=test_db
DB_USER=test_user

# make sure postgres is not running before using these commands. `ps aux | grep postgres`
# init db with main_db as the main directory. (Assume main_db doesn't already exist)
initdb -D $DB_DIR

# start log file
pg_ctl -D $DB_DIR -l db_logfile start

# create a user. add --pwprompt if you want to add a password
createuser --encrypted $DB_USER

# create the db named test_db with with test_user as the owner
createdb --owner=test_user $DB_NAME


