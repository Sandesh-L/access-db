#ASSUMING setup.sh is already run

DB_DIR=postgres_db

# Load environment variables
set -a 
source .env
set +a

# Check if required variables (db users and passwords) are set 

if [ -z "$DB_ADMIN_USER" ] || [ -z "$DB_ADMIN_PASS" ] || [ -z "$DB_EDIT_USER" ] || [ -z "$DB_EDIT_PASS" ] || [ -z "$DB_VIEW_USER" ] || [ -z "$DB_VIEW_PASS" ]; then
    echo "Error: DB_ADMIN_USER, DB_ADMIN_PASS, DB_EDIT_USER, DB_EDIT_PASS, DB_VIEW_USER, DB_VIEW_PASS must be set in .env file"

else


# make sure postgres is not running before using these commands. `ps aux | grep postgres`
# stop the server/db using `pg_ctl stop -D ./postgres_db/`
# init db with main_db as the main directory. (Assume main_db doesn't already exist)
initdb -D $DB_DIR

# start the db and log file
pg_ctl start -D $DB_DIR -l db_logfile

# Wait for the database to be ready
until pg_isready -q
do
    echo "Waiting for database to be readay..."
    sleep 1
done

# create admin user with superuser privilages
createuser --superuser $DB_ADMIN_USER

# Set admin user's password
psql -d postgres -c "ALTER USER $DB_ADMIN_USER WITH PASSWORD '$DB_ADMIN_PASS';"

# create the db named $DB_NAME with with DB_ADMIN_USER as the owner
createdb --owner=$DB_ADMIN_USER $DB_NAME

# To stop the postgres server use:
# pg_ctl stop -D ./postgres_db/ -m smart

# Create SQL commands to add users and permissions
SQL_COMMANDS=$(cat <<EOF

-- Create a user with read-only access
CREATE USER $DB_VIEW_USER WITH PASSWORD '$DB_VIEW_PASS';

-- Grant connect permission on the database
GRANT CONNECT ON DATABASE $DB_NAME TO $DB_VIEW_USER;

-- Grant usage on schema (assuming public schema)
GRANT USAGE ON SCHEMA public TO $DB_VIEW_USER;

-- Grant select permission on all tables in the schema
GRANT SELECT ON ALL TABLES IN SCHEMA public TO $DB_VIEW_USER;

-- Grant select permission on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO $DB_VIEW_USER;

-- Create a user with edit access (but no schema modification rights)
CREATE USER $DB_EDIT_USER WITH PASSWORD '$DB_EDIT_PASS';

-- Grant connect permission on the database
GRANT CONNECT ON DATABASE $DB_NAME TO $DB_EDIT_USER;

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO $DB_EDIT_USER;

-- Grant select, update, insert, delete permissions on all existing tables
GRANT SELECT, UPDATE, INSERT, DELETE ON ALL TABLES IN SCHEMA public TO $DB_EDIT_USER;

-- Grant select, update, insert, delete permissions on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public 
GRANT SELECT, UPDATE, INSERT, DELETE ON TABLES TO $DB_EDIT_USER;

-- Revoke create permission on the schema to prevent table creation
REVOKE CREATE ON SCHEMA public FROM $DB_EDIT_USER;
EOF
)

# Execute SQL command to create users
echo "$SQL_COMMANDS" | PGPASSWORD=$DB_ADMIN_PASS psql -U $DB_ADMIN_USER -d $DB_NAME

echo "Users created and permissions udpated."

fi

