#!/bin/bash

set -euo pipefail

CONF="$(pwd)/config.json"

function info() {
	echo "INFO: ${@}"
}

info "Reading mysql values from ${CONF}"
MYSQL_HOST=$(jq -r '.db.host' ${CONF})
MYSQL_USER=$(jq -r '.db.user' ${CONF})
MYSQL_PASSWORD=$(jq -r '.db.password' ${CONF})
DATABASE_NAME=$(jq -r '.db.database' ${CONF})
MYSQL_PORT=$(jq -r '.db.port' ${CONF})

info "Creating the database"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $DATABASE_NAME;"

info "Executing initial query"
mysql -h $MYSQL_HOST -P $MYSQL_PORT -u $MYSQL_USER -p$MYSQL_PASSWORD -e "USE $DATABASE_NAME; \
CREATE TABLE IF NOT EXISTS products (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(50),
    name VARCHAR(100),
    manufacturer VARCHAR(100),
    category VARCHAR(100),
    storage_place VARCHAR(100),
    amount DECIMAL(10,2),
    expiry_type VARCHAR(100),
    expiry_date DATE,
    unit VARCHAR(20)
); \
CREATE TABLE IF NOT EXISTS product_templates (
    barcode VARCHAR(50) NOT NULL PRIMARY KEY,
    name VARCHAR(100),
    manufacturer VARCHAR(100),
    category VARCHAR(100),
    storage_place VARCHAR(100),
    amount DECIMAL(10,2),
    expiry_type VARCHAR(100),
    unit VARCHAR(20)
);"

info "Success, now run \"npm i && node app.js\" "

