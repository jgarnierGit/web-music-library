from celery import shared_task
from .consts import MUSIC_PATH, AUDIO_EXTENSIONS
from .models import Music
import os
from .services.filesystem import updateDb


@shared_task(name="parse_filesystem", bind=True)
def parse_filesystem(self, force_update):
    task = self
    updated = parse_tree(MUSIC_PATH, force_update, task)
    return updated


def parse_tree(path, force_update, task, updated=0):
    try:
        for p in os.listdir(path):
            p_path = os.path.join(path, p)
            if os.path.isdir(p_path):
                updated = parse_tree(p_path, force_update, task, updated)
            elif (
                os.path.isfile(p_path)
                and os.path.splitext(p_path)[1] in AUDIO_EXTENSIONS
            ):
                existing_music = Music.objects.filter(path=p_path)
                if not existing_music:
                    music = updateDb(p, p_path, force_update)
                    if music["saved"]:
                        updated += 1
                        task.update_state(
                            state="PROGRESS",
                            meta={"current": updated},
                        )
    except Exception as e:
        print(f"Unexpected error: {e}")
    return updated
