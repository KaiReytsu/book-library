export $(grep -v '^#' .env | xargs)
psql $POSTGRES_DB_NAME $POSTGRES_USER -h $POSTGRES_HOST