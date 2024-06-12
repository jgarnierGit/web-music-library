<template>
  <MusicTree v-model="library" />
</template>
<script setup lang="ts">
import { reactive } from 'vue';
import type { Folder } from '~/commons/interfaces';
import MusicTree from '~/components/MusicTree.vue';

const content: Folder = { id: '', name: '', folders: [], musics: [], path: '' };

const content_test = {
  "id": "/music2",
  "name": "music",
  "path": "/music",
  "folders": [
    {
      "id": "/music/Anime BO1",
      "name": "Anime BO",
      "path": "/music/Anime BO",
      "folders": [],
      "musics": [
        {
          "id": "9a2dcbaa-1d35-4c55-9a04-28b546085b57",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "opening01_fullversion.mp3",
          "path": "/music/Anime BO/opening01_fullversion.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "787628d4ab31ac49f4dbf97faee2bea5d080cf4433aac42d22c56466a6db4d59"
        }
      ]
    },
    {
      "id": "/music/Chillout Abstract-Trip Hop NuJazz1",
      "name": "Chillout Abstract-Trip Hop NuJazz",
      "path": "/music/Chillout Abstract-Trip Hop NuJazz",
      "folders": [],
      "musics": []
    },
    {
      "id": "/music/Classique1",
      "name": "Classique",
      "path": "/music/Classique",
      "folders": [],
      "musics": [
        {
          "id": "d9604337-e2a6-43c2-895c-986dfb8097ba",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "RIMSKI-KORSAKOV - Le vol du bourdon.mp3",
          "path": "/music/Classique/RIMSKI-KORSAKOV - Le vol du bourdon.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "42e1ab7a290391b0718d8bb71719292adef877612f9df3baf82ffbafc5a658e7"
        },
        {
          "id": "022bf72e-3fb0-4c16-83c9-9d1171bad1fb",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "saint saens - danse macabre.mp3",
          "path": "/music/Classique/saint saens - danse macabre.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "2b1c86c0ec355efe0200227719c3700248264f2eaade77b1dc985fee9cfe010a"
        },
        {
          "id": "a6da1303-979d-4091-aeec-096c14025e16",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Symphonie espagnole en ré mineur pour violon et orchestre Op.21  I Allegro non troppo.mp3",
          "path": "/music/Classique/Symphonie espagnole en ré mineur pour violon et orchestre Op.21  I Allegro non troppo.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "e1498133e18fa899820681256169a333a4d9c07a6122080d8fe005eb4c5faac7"
        }
      ]
    },
    {
      "id": "/music/Downtempo Ambient Psydub1",
      "name": "Downtempo Ambient Psydub",
      "path": "/music/Downtempo Ambient Psydub",
      "folders": [],
      "musics": []
    },
    {
      "id": "/music/Jazz Afrobeat Fusion World1",
      "name": "Jazz Afrobeat Fusion World",
      "path": "/music/Jazz Afrobeat Fusion World",
      "folders": [],
      "musics": []
    },
    {
      "id": "/music/Medtempo Trance Chillstep1",
      "name": "Medtempo Trance Chillstep",
      "path": "/music/Medtempo Trance Chillstep",
      "folders": [],
      "musics": [
        {
          "id": "0e33de0c-2d4b-4294-8caa-d6b74e29096f",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Electrocado - Ahuacatl.mp3",
          "path": "/music/Medtempo Trance Chillstep/Electrocado - Ahuacatl.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "a29121e190122d05721c3634ad132883dd552550cecdf83af33339fa83ffaab1"
        }
      ]
    },
    {
      "id": "/music/Pop-rock Progressive Folk Folk-Punk1",
      "name": "Pop-rock Progressive Folk Folk-Punk",
      "path": "/music/Pop-rock Progressive Folk Folk-Punk",
      "folders": [],
      "musics": [
        {
          "id": "2c4a51d6-2af2-454e-a8a7-94efc3b4d1b2",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Depeche Mode - Enjoy The Silence.mp3",
          "path": "/music/Pop-rock Progressive Folk Folk-Punk/Depeche Mode - Enjoy The Silence.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "32c645899cef4101ded58c17fbb519c29d32d70e0778925640bd6febbaeccb37"
        },
        {
          "id": "12c3778d-d05c-4dd8-bba0-e5ad4407b202",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Jack Johnson - Good people.mp3",
          "path": "/music/Pop-rock Progressive Folk Folk-Punk/Jack Johnson - Good people.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "9a3316df2e7ef6eeba6cf1adebe8c06e84ba940820a9cfceb2027eaaebbdf887"
        },
        {
          "id": "8fbb8c99-5efa-451e-931f-1ce87b85ec8f",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Jack Johnson - Upside Down.mp3",
          "path": "/music/Pop-rock Progressive Folk Folk-Punk/Jack Johnson - Upside Down.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "4d329be8573dd1e3eb6df98f9d81f1a88abf7daeff2ceb30f17fb6c0f488a7ed"
        },
        {
          "id": "4e54545d-934a-4fd4-b5bb-d96b431b310d",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Midnight oil - Beds Are Burning.mp3",
          "path": "/music/Pop-rock Progressive Folk Folk-Punk/Midnight oil - Beds Are Burning.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "262a2d7ff9ba67822d21e949e0e989d13a85b6308851488fc44dab9c34eefe04"
        },
        {
          "id": "9619706b-30d1-4e12-af1c-099fec3a62e8",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Moon Martin - Bad news.mp3",
          "path": "/music/Pop-rock Progressive Folk Folk-Punk/Moon Martin - Bad news.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "07704246587f9237866518b145abc596c01817f6a977d0bf204b1139c5418697"
        },
        {
          "id": "03698042-0e10-430d-b3b7-18f4e2df56b8",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "tanger - la fee de la foret.mp3",
          "path": "/music/Pop-rock Progressive Folk Folk-Punk/tanger - la fee de la foret.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "7edf1e3ea91e9287b197d10f3a59e3d2e96f62b4439df3e1ba73e39378bbb901"
        },
        {
          "id": "731ee141-971c-4d5a-b244-81c9e22740e1",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "The Who - Who Are You.mp3",
          "path": "/music/Pop-rock Progressive Folk Folk-Punk/The Who - Who Are You.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "8ac1f631a1e5cc2f093105023784f686379ff3cf50636588f594a8e8bdde33d2"
        }
      ]
    },
    {
      "id": "/music/Post-rock metal  Math-Rock Grunge1",
      "name": "Post-rock metal  Math-Rock Grunge",
      "path": "/music/Post-rock metal  Math-Rock Grunge",
      "folders": [],
      "musics": []
    },
    {
      "id": "/music/Psy Goa Tribecore Raggatek1",
      "name": "Psy Goa Tribecore Raggatek",
      "path": "/music/Psy Goa Tribecore Raggatek",
      "folders": [],
      "musics": [
        {
          "id": "3120ef8e-e56e-4223-8f1f-37c150f7ea2f",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "TakaTuka & GehLekTek - Shiko.mp3",
          "path": "/music/Psy Goa Tribecore Raggatek/TakaTuka & GehLekTek - Shiko.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "e4fedc4d1450ed4890f60a7372e1ba3d8185528e6474f06cb8fe48abd3575577"
        }
      ]
    },
    {
      "id": "/music/Punk Celtic1",
      "name": "Punk Celtic",
      "path": "/music/Punk Celtic",
      "folders": [],
      "musics": [
        {
          "id": "b2a64c87-26ef-4ed7-9f67-08e96fdef14b",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Hanover Saints - masquerade.mp3",
          "path": "/music/Punk Celtic/Hanover Saints - masquerade.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "73447ba709dea067accde1a8081f4c331dc5e4bade44bb5bfadc4d631bc48743"
        },
        {
          "id": "d68919e7-0322-465d-89af-ccf6e16ef7c4",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "jetsex - invisible minority.mp3",
          "path": "/music/Punk Celtic/jetsex - invisible minority.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "0aa6baa5ed8dcd3283e2a95eb24e1a629c8cdbff3a8b9968b9db844359bbfcf4"
        }
      ]
    },
    {
      "id": "/music/Punk-Rock Metal Hard-Rock1",
      "name": "Punk-Rock Metal Hard-Rock",
      "path": "/music/Punk-Rock Metal Hard-Rock",
      "folders": [],
      "musics": [
        {
          "id": "d8241c2f-c0ca-4544-a658-d9d0a9938130",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "el presidente-Without You.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/el presidente-Without You.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "3cb0b881fabb76dd453c71e19faba034c5d969c414586764addcad6cd719bcd5"
        },
        {
          "id": "5a28f300-725e-4e15-8a76-bc2a0798855e",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Fake It.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Fake It.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "495698fda4bfad69d8cddde4dbcbeccac45c29867be4d78eea10e6549be7cd91"
        },
        {
          "id": "d85f0323-ebc8-4bcf-801d-676773245d82",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Fall Out Boy - Dance Dance.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Fall Out Boy - Dance Dance.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "675272048717194271b7ce4255968a0d2be5b372840ec8a0fa507e9a046136b4"
        },
        {
          "id": "2ed8ed52-44d8-4ec9-8738-e23dcf9e97c9",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "hellogoodbye - here (in your arms).mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/hellogoodbye - here (in your arms).mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "2726edc0d52858d2633a6d147943a124e66ea46ab98e75df81cab6881b0fcbff"
        },
        {
          "id": "8be832e2-36b0-4f38-b7ce-b8b18d1c50ad",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Hush Puppies - You're gonna say yeah.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Hush Puppies - You're gonna say yeah.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "b6c5c80a3ceec01ce4d462236b907a9c10ed50c881797b9ddcc96b9cc7a5fd98"
        },
        {
          "id": "165f8784-c2dd-4606-b7a2-e4853ee488f3",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Jamiroquai - Deeper Underground.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Jamiroquai - Deeper Underground.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "b0f690b897fe1dc265b7976daa5e9e02487cd57284b28ddf79ac5f82360803b0"
        },
        {
          "id": "5c96d80b-1bad-4511-a6db-60abc7ed3bfd",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Joan Jett & the Blackhearts - I Love Rock And Roll.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Joan Jett & the Blackhearts - I Love Rock And Roll.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "4155a4517ba5790e11361fabd980d3d2d424a57b9bd20b04cb44ee84ddcf514b"
        },
        {
          "id": "2de89b9a-fc6e-4bef-a9a1-7635b31f9cf7",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Kaiser Chiefs - Ruby.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Kaiser Chiefs - Ruby.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "8828de4f7a26499e0a1775be7370490f80a4678cc4ecf64f8f262e13456b1cd7"
        },
        {
          "id": "58a3e358-0380-4cbf-b103-60afaaba389b",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Kiss - I Was Made For Loving You (Pub Coca Cola 2005).mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Kiss - I Was Made For Loving You (Pub Coca Cola 2005).mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "a26dcc1efe5311e38dcec9640456e514b81fa9f9069e1afdcfacd455641ba4b8"
        },
        {
          "id": "771b4092-ebfa-4b4b-a757-0ac13998c146",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Megadeth - Trust.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Megadeth - Trust.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "2208484286582c9507c474d60dc5dbaf523f0a52f630366440bea61bce007606"
        },
        {
          "id": "39c354e4-245c-4580-8752-55d47ad458fc",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "No Doubt - Don't Speak.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/No Doubt - Don't Speak.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "a07a18632829822ad58193ec0b7c6e0bf4ae21f3c11125d97572f6bec8a7a176"
        },
        {
          "id": "14c26e42-d1f9-4877-957e-f1d9a417189e",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Oasis - Wonderwall.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/Oasis - Wonderwall.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "f26e1e8ba18459f7fe0242369dac710302cc984e16952d7ed677a60332a3384a"
        },
        {
          "id": "31e8b4d2-6867-4fe6-88ef-8b3bb1f287f6",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "RamJam - Black Betty.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/RamJam - Black Betty.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "f6184806e12d5cb0bd56144712e7b55fa40c443657eeaf591d9a004ea2f43541"
        },
        {
          "id": "8fdb85cb-d159-4619-a170-802192ab8051",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "the automatic - monster.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/the automatic - monster.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "221c95f95aba939f0c70eb04520a429ebed5667fd5f34d48ffcb205100daae80"
        },
        {
          "id": "51e3e237-7d3f-440d-967e-35cb2f1da86e",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "The Rasmus-In the shadow.mp3",
          "path": "/music/Punk-Rock Metal Hard-Rock/The Rasmus-In the shadow.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "f1d7a77e41d279c29ae359a2acd7929625ae7d467b8238f25f6007bad65ee516"
        }
      ]
    },
    {
      "id": "/music/Rap Hip hop1",
      "name": "Rap Hip hop",
      "path": "/music/Rap Hip hop",
      "folders": [],
      "musics": [
        {
          "id": "533d8184-cb18-4071-a0ce-01c5028f4b2e",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Freestyler.mp3",
          "path": "/music/Rap Hip hop/Freestyler.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "ef1adea4c527bd808a152acbb68b6b9314e3ee5d7b73a48052532a95854f9efd"
        }
      ]
    },
    {
      "id": "/music/Ska Reggae Dub1",
      "name": "Ska Reggae Dub",
      "path": "/music/Ska Reggae Dub",
      "folders": [],
      "musics": [
        {
          "id": "762ab560-7de5-4d32-895c-49a8d85db59b",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Gadjo loco - the house of the rising sun.mp3",
          "path": "/music/Ska Reggae Dub/Gadjo loco - the house of the rising sun.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "db71fa2ab8ec5c1abcfa0e5a9f00ed05c0af798cb2c670cc5d9257324d272912"
        },
        {
          "id": "7a3aea88-435a-4944-a171-88681e536409",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Pomme De Terre.mp3",
          "path": "/music/Ska Reggae Dub/Pomme De Terre.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "186e719b739d12b8493cdd2f1f3b69e4726cf3e928efbcc53bf6e2c130cd2688"
        }
      ]
    },
    {
      "id": "/music/Techno Trance House1",
      "name": "Techno Trance House",
      "path": "/music/Techno Trance House",
      "folders": [],
      "musics": [
        {
          "id": "7b7e8559-d084-451d-9fec-f7703247f9bd",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Chemical Brothers - Star Guitar.mp3",
          "path": "/music/Techno Trance House/Chemical Brothers - Star Guitar.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "b75f5ce51ec46d0b997529c4744056ca7fcc98648a51557f93f02bc7d9ac1ddb"
        },
        {
          "id": "b899f743-c365-4185-b9aa-12832be06304",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Gabber Mafia - Gabber Mafia.mp3",
          "path": "/music/Techno Trance House/Gabber Mafia - Gabber Mafia.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "3a52a119d343889de3dc8e968ec21097665ca329576217278774971a718ceeb8"
        },
        {
          "id": "dffc0bd5-de90-4de3-baf9-0385bada7ec1",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Sandstorm - Darude.mp3",
          "path": "/music/Techno Trance House/Sandstorm - Darude.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "98984e4cf70f2076da82090425f14060c04dff4ef79fceab210fe468bafb119b"
        },
        {
          "id": "493cffc2-b7b4-4d5b-a69f-08e595266d41",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Vladgorythm suicide.mp3",
          "path": "/music/Techno Trance House/Vladgorythm suicide.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "d04cc2768b9bbd745765968dcec991f2fb24076690952908336c485fdcd68337"
        }
      ]
    },
    {
      "id": "/music/Variete francaise1",
      "name": "Variete francaise",
      "path": "/music/Variete francaise",
      "folders": [],
      "musics": [
        {
          "id": "92feb2db-07d6-4471-b4da-0a0163c486ca",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "01-MALOH _ C'EST GRAVE DOCTEUR _.mp3",
          "path": "/music/Variete francaise/01-MALOH _ C'EST GRAVE DOCTEUR _.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "12eebbdbb783e79d4fef035b401625d587857ecd36a3cf8653b8542926fcabcf"
        },
        {
          "id": "144cd8c7-a5d6-4914-a9c1-19e3cf9f2969",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "06-MALOH _ DRAPS DESSUS DRAPS DESSOUS.mp3",
          "path": "/music/Variete francaise/06-MALOH _ DRAPS DESSUS DRAPS DESSOUS.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "f51226dc47a9f53d4ed3414613ed0b90ee1fb89f5592e9694f5ac3ed3c8363d8"
        },
        {
          "id": "b218605f-3a75-4c00-bc1d-8f9598a3775c",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Calogero - En apesenteur.mp3",
          "path": "/music/Variete francaise/Calogero - En apesenteur.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "901c64b13b0ce377a98823e61701eaa20530f27e5c344b857e14eeb19b3d5d2d"
        },
        {
          "id": "068216e3-9aac-4937-9768-7ca07a5010a3",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "le banquet.mp3",
          "path": "/music/Variete francaise/le banquet.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "93a4f38d1262870c0190befe05d4cb3c195a1f2a35c211943fa5026cf8b10320"
        },
        {
          "id": "ae7ed945-c6cc-41aa-9740-013d2c7effae",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Steve Waring - le matou revient.mp3",
          "path": "/music/Variete francaise/Steve Waring - le matou revient.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "b6586f73dc07887e2ce12431ce79e7269dca9bdd3e10553c52c50e86b43c61e2"
        }
      ]
    },
    {
      "id": "/music/Zautres1",
      "name": "Zautres",
      "path": "/music/Zautres",
      "folders": [],
      "musics": [
        {
          "id": "4bcab6c0-c388-4a78-971a-502cb30ffd3a",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "15-D-.mp3",
          "path": "/music/Zautres/15-D-.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "e561dce6eb6c6267599cacf33b081280afe0d7889eafb151e87b54b4d0adac5d"
        },
        {
          "id": "98b00471-8ff4-446d-9e6b-944144cb3852",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "99luftballons.mp3",
          "path": "/music/Zautres/99luftballons.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "1f6beb1800233c394984e924f1cf355f859a71900bbb2269d3988331dc065d48"
        },
        {
          "id": "5c63cda6-5df3-4e56-aaaa-a60efd7b1bce",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Andreas Johnson - Glorious.mp3",
          "path": "/music/Zautres/Andreas Johnson - Glorious.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "69f8073635deacee9daf0e96bdb3df27cfb97f3cc5972cf305ef011cdd173449"
        },
        {
          "id": "d628573d-50cd-4a96-878a-20ae5241356f",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Beatles - John Lennon - Imagine.mp3",
          "path": "/music/Zautres/Beatles - John Lennon - Imagine.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "ca69396ceb2539e9eed0f11d4aba7465ddf6315d92a9482caee1f67675c15698"
        },
        {
          "id": "e641af4f-4d19-4b58-a45a-03b620b3f308",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Cardigans - My Favorite Game.mp3",
          "path": "/music/Zautres/Cardigans - My Favorite Game.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "ef59b995103d6f022131e136717f4e31c5081972ba476f125c539ca60acb0379"
        },
        {
          "id": "399accad-a6da-4ea3-a69d-c37b532b705c",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Corona - Rythm Of The Night.mp3",
          "path": "/music/Zautres/Corona - Rythm Of The Night.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "6e3c2293e7303ef1f88f456781c44edc8a392922092932fa1c3529c0c5b11e95"
        },
        {
          "id": "f74eafba-a24c-4c18-b7aa-290286ba4a17",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Daniel Balavoine - La ziza.mp3",
          "path": "/music/Zautres/Daniel Balavoine - La ziza.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "116fd3b54b73f9ca5c4dae418898fc7ebf25919b88cd0ea897ed19deda1c8677"
        },
        {
          "id": "0aaee5b3-7572-41e4-b03e-26c42183d76c",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "DJ JIM - Electro Speed XIII.mp3",
          "path": "/music/Zautres/DJ JIM - Electro Speed XIII.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "f7d0da65562ef2029834a3034c37dea252b233153003435192f6314bda9d145e"
        },
        {
          "id": "97dd246f-be22-4804-a71b-8c2273132867",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "eurythmics - sweet dreams.mp3",
          "path": "/music/Zautres/eurythmics - sweet dreams.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "e70f2263bc4a611df5abeea61d1ebf75b152d622211a50e2f9558de35ad80334"
        },
        {
          "id": "02671024-5068-460f-a905-672d3654cca2",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "hoosiers - worried about ray.mp3",
          "path": "/music/Zautres/hoosiers - worried about ray.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "95b7ab4a6354933674a82ca0ab495867780696c8a1b4e772a77bab91d3addd04"
        },
        {
          "id": "56c361dd-6253-4e40-9463-7254420c9744",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "jehro - i want love.mp3",
          "path": "/music/Zautres/jehro - i want love.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "88c02cc66ff37b73076ef9543d12ba8e826dbb57a3b7600934ad2ae9ffaa85f9"
        },
        {
          "id": "497a74e3-f647-47b5-8484-6adcfd15934a",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "jen reve encore.mp3",
          "path": "/music/Zautres/jen reve encore.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "4417bf0bd2957558742e4b96e03bb0323626a4534c22aab6e1461fc49ecade67"
        },
        {
          "id": "af8aa0f4-7ecc-4845-8afd-d63399da9fcd",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Joe Dassin - L ete Indien.mp3",
          "path": "/music/Zautres/Joe Dassin - L ete Indien.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "df160890d87f77d5c49ced5f33a7d04b0976c93fb2b41953e0d4bab063e1c44e"
        },
        {
          "id": "46d6807b-3bc9-4a9c-baa3-4343379c210e",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "John Powell - Assassin's Tango.mp3",
          "path": "/music/Zautres/John Powell - Assassin's Tango.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "243e97ede3a3ca3d1ac2c29e855e821f0acb287bccd4a98f650e381d728b3e6d"
        },
        {
          "id": "1866108f-8c90-478b-a0ec-a6d9271f15a5",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "la dance des sabres.mp3",
          "path": "/music/Zautres/la dance des sabres.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "46bd986c6bc869664915082da7e8fff2a445429fe299f1d081bb2afd1a9c573c"
        },
        {
          "id": "1484a402-91ab-4480-bbe9-b58c776be6df",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Lipps Inc - Funky Town.mp3",
          "path": "/music/Zautres/Lipps Inc - Funky Town.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "5892de290df856483ba73a1dff19ca8cb548e87aae5e2af816fec0325edf5b85"
        },
        {
          "id": "eec86499-bdd6-42db-9b9b-e4df98e71daf",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "My generation.mp3",
          "path": "/music/Zautres/My generation.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "056bf4fe9f1a9f2ae5754d9e210e6cdf978bd3cb6c48118476392b28b56ebf43"
        },
        {
          "id": "39e09dcb-ed9e-48ae-8d98-21fd103e87b9",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Plastic Bertrand - Ca plane pour moi.mp3",
          "path": "/music/Zautres/Plastic Bertrand - Ca plane pour moi.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "148476c135dcfffa8b88102defaa1388bf6aa009d783e95a655c54b6bd9351fd"
        },
        {
          "id": "7caa0f7d-0826-47e3-a116-6d0634ff7589",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Rayman 3.mp3",
          "path": "/music/Zautres/Rayman 3.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "2ada62ab2d3128a62546e3f76e8af83f9d67178e3716ad775286be32b966a6b5"
        },
        {
          "id": "97bf201a-7ed8-4510-ab76-1614d44830f5",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Richard Wagner - La Chevauchee des Walkyries.mp3",
          "path": "/music/Zautres/Richard Wagner - La Chevauchee des Walkyries.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "9c4ad4a7e50c0db93041b86045cf68b89f393796c8ef5fa7554a1834b66417b8"
        },
        {
          "id": "a6072a5e-b5c4-4a29-833e-dc0a702b8975",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Robbie William Kylie Minoque - Kids.mp3",
          "path": "/music/Zautres/Robbie William Kylie Minoque - Kids.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "7494f3abcd8c1ace7d33f7ab7f1c8a0f85fd7aab042e02bbadb669a6f6e24554"
        },
        {
          "id": "32c0640d-5579-436c-8a58-367535f8124d",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Simple Plan - Welcome to My Life.mp3",
          "path": "/music/Zautres/Simple Plan - Welcome to My Life.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "916ef5be29930d1f1e96d37fa7943f84e005078552218c8f2014991e753e8793"
        },
        {
          "id": "dbe5ac95-3b9a-4451-9912-910ee50ddcd8",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Superbus - Butterfly.mp3",
          "path": "/music/Zautres/Superbus - Butterfly.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "05b3d3a31e8845f2bb53c769d5ad041376925bdd513f1c5013d9955cc52132eb"
        },
        {
          "id": "2346e976-70b2-4fc2-bd94-022ef7243a28",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Superbus_Pop'n gum.mp3",
          "path": "/music/Zautres/Superbus_Pop'n gum.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "2505126f5e7e5271d5c9a6f7a00f3bfeb68b93fb96c9aa0a68d38003e071792a"
        },
        {
          "id": "1ca02b14-75cf-449d-a0e9-d34b2fb1e357",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "sweet home alabama.mp3",
          "path": "/music/Zautres/sweet home alabama.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "31dd6c004a6383873a41882ce5601a9dd97431a124cfeeb075758ec085eab2a1"
        },
        {
          "id": "10958d20-f02e-4fee-b66c-47f61f37c46c",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "The Verve - Bittersweet Symphony.mp3",
          "path": "/music/Zautres/The Verve - Bittersweet Symphony.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "c4e510581f958953d572b5f040015110550f09d891414896f5fcf48bbcc500b8"
        },
        {
          "id": "74bf1dff-4318-4b9b-b013-409603625ee5",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Track No01.mp3",
          "path": "/music/Zautres/Track No01.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "8274eea97f42b0d08d1ef6c658e9959db1eb022d6cc7da9d51050376cae01d12"
        },
        {
          "id": "cb7b82d4-521f-4b9c-9faa-1e022d48c32e",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Video Killed the Radio Star.mp3",
          "path": "/music/Zautres/Video Killed the Radio Star.mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "16d6052746d72228f175d0002511600e881fcbbe322efddd59a56bb999e2959c"
        },
        {
          "id": "39082dfb-fc54-4768-80ad-0e98fc19f3be",
          "artist": {
            "id": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "name": "fake_artist",
            "geom": null
          },
          "album": {
            "id": "a79dbd2f-ac58-4894-8ddd-fdcbdfbae6d4",
            "name": "fake_album",
            "date": null,
            "artist": "2aca443c-5eb5-41df-ae8d-f2f09757fdaa",
            "genre": null
          },
          "name": "Village People - YMCA (Disco Oldies).mp3",
          "path": "/music/Zautres/Village People - YMCA (Disco Oldies).mp3",
          "track": 0,
          "duration": 0,
          "bpm": null,
          "last_played": null,
          "count_played": 0,
          "count_skipped": 0,
          "checksum": "e652786912c803d18929803c3eb18ad77e610597f5b7f74886e4e1da68a556ad"
        }
      ]
    }
  ],
  "musics": []
};
const library = reactive(content_test);
</script>