#!/bin/bash

source backup_db.sh

ssh root@vps.pesadoselnorte.com.ar 'source /root/get_db_docker.sh'

scp root@vps.pesadoselnorte.com.ar:/root/db.new.sqlite3 /mnt/d/DEV/extras_pesados/new_db/db.sqlite3
