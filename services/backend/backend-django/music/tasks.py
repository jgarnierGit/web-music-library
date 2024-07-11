from celery import shared_task
from .consts import MUSIC_PATH, AUDIO_EXTENSIONS
from .models import Music
import os
from .services.filesystem import update_bulk_music_db, get_model_to_save


@shared_task(name="parse_filesystem", bind=True)
def parse_filesystem(self, force_update):
    task = self
    updated = parse_tree(MUSIC_PATH, force_update, task)
    return updated


def parse_tree(path, force_update, task, updated=0):
    try:
        folder_to_process = []
        bulk_musics = []
        for p in os.listdir(path):
            p_path = os.path.join(path, p)
            if os.path.isdir(p_path):
                folder_to_process.append(p_path)
            elif (
                os.path.isfile(p_path)
                and os.path.splitext(p_path)[1] in AUDIO_EXTENSIONS
            ):
                existing_music = Music.objects.filter(path=p_path)
                if not existing_music or force_update:
                    bulk_music = get_model_to_save(p, p_path)
                    if bulk_music:
                        bulk_musics.append(bulk_music.get("music"))

        if len(bulk_musics) > 0:
            result = update_bulk_music_db(bulk_musics, force_update)
            updated += len(result)
            task.update_state(
                state="PROGRESS",
                meta={"current": updated},
            )
        for p_path in folder_to_process:
            updated = parse_tree(p_path, force_update, task, updated)
    except Exception as e:
        print(f"Unexpected error: {e}")
    return updated
