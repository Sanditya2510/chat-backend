-- Use this to modify in future
CREATE DATABASE sas_chat;
CREATE USER admin WITH PASSWORD 'admin123';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE sas_chat TO admin
