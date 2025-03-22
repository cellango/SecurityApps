docker stop appinventory-frontend
#docker exec appinventory-db psql -U postgres -d appinventory -c DROP SCHEMA public CASCADE; CREATE SCHEMA public;
docker stop appinventory-backend
docker exec appinventory-db psql -U postgres -c "DROP DATABASE appinventory;"\n
docker exec appinventory-db psql -U postgres -c 'CREATE DATABASE appinventory;'
make rebuild
