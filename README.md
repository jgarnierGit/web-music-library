# Music Library player

Building my own web interface and enjoying my music while coding :)

If you want a full featured webplayer based on Winamp experience, go check [webamp](https://github.com/captbaritone/webamp)

## Overview

Frontend : 
  - App : [Vue3](https://vuejs.org/), [Nuxt3](https://nuxt.com/), [Pinia](https://pinia.vuejs.org/)
  - Component Framework : [Vuetify3](https://vuetifyjs.com/)
  - Music Vizualiser : [projectM](https://github.com/projectM-visualizer/projectm) via [webAssembly](https://webassembly.org/)
  - Geospatial Map : [Leaflet](https://leafletjs.com/) with [Turf.js](https://turfjs.org/) and [shpjs](https://www.npmjs.com/package/shpjs)

Backend : 
  - Server : [python3](https://www.python.org/), [Django](https://www.djangoproject.com/), [Nginx](https://nginx.org/)
  - Database : [PostgreSQL](https://www.postgresql.org/), [PostGIS](https://postgis.net/)

## Architecture Diagram

[WIP]

## Features 

 - Music library accessing in readonly mode to your local library
 - Database persistency with metadata exposition
 - Geospatial music localizer editor & filtering - WIP  (ne_110m_admin_0_countries)
 - ProjectM Milkdrop vizualisation

Musics from your fileSystem are saved in the database on the first reach.

For now, music files can be populated with [/filesystem/list](http://localhost:8000/filesystem/list) endpoint.

A checksum is calculated based on music name, artist name and album name, to make the database resilient to filesystem changes.

 - metadata editor (db persistency) :
   - In addition of reading music file metadata, you can fetch artist country via [musicbrainz](https://musicbrainz.org). If the match has a unique result with a score of 100, it will be saved automatically, otherwise you'll have to check and save.

## Setup

[Docker](https://www.docker.com/)

## Configuration

edit .env example before first launch :

 - `MUSIC_LIBRARY_PATH` : path to your music folder
 - `MUSIC_PATH_MAX_LENGTH` : default 500 character, increase that number if your music paths exceed this value, then restart backend.
 - `PG_DATA` : database persistency.
 - `API_HEADER_MAIL` : mandatory to use properly musicbrainz.org API

## Start up

`docker compose up`

- frontend (`http://localhost:3000`)
- backend (`http://localhost:8000`)
  - Django admin (`localhost:8000/admin`)
    - root/root
- Nginx serving your music filesystem(`http://localhost:8081/music`)
- database access (`0.0.0.0:54333`)
  - postgres/postgres
  - database and schema : `music`.`public`
  - external database manager recommended [DBeaver](https://dbeaver.io/), for as long as I don't provide pgadmin container.

### Notes

`backend` may fails to connect to database as it doesn't wait enough for the first db init :

 - Wait for the db container log line `LOG:  database system is ready to accept connections`. It may take a while and you may see database stopping and restarting in the process.
 - Then run `docker compose restart backend`.

## dev Notes

front end dev, set this variable to disable API calls if you do not plan to work with the server launched

```
  vite: {
    define: {
      VUE_APP_MOCK_SERVER: true
    },
```

# Thanks

 - ProjectM Webassembly integration :
   
   [evoyy:projectm-webgl-demo](https://github.com/evoyy/projectm-webgl-demo) for its ProjectM emscripten generation.