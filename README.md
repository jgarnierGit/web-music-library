
# run

`docker compose up`

backend may fails to connect to database as it doesn't wait enough for the first db init. 

Wait for the db log line `LOG:  database system is ready to accept connections`. 
You may then want to run `docker compose restart`.

This software is using a postgres / postgis database

POSTGRES_DATA : storing postgres data

connect with external database manager (i.e Dbeaver)
0.0.0.0:54333
postgres / postgres

core logic will be populated in 'music.library' database and schema

music files can be populated with [/filesystem/list](http://localhost:8000/filesystem/list) endpoint for now,
a checksum is calculated based on music name, artist name and album name, to make the database resilient for filesystem changes.


django admin

localhost:8000/admin
root/root

configuration
`MUSIC_LIBRARY_PATH` : path to your music folder
`MUSIC_PATH_MAX_LENGTH` : default 500 character, increase that number if your music paths exceed this value
then restart backend container.

nginx to access music folder via web browser
localhost:8081/music