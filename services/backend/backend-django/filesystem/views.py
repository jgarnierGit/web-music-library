import os
from django.http import JsonResponse

MUSIC_PATH = "/music_library"
# Audio file extensions
AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg", ".flac"]


def get_tree(path, level):
    """
    edge cases :
        * Not handling hidden files / folders
        * Not following symlinks (os.scandir)
        * Large directories may cause out of memory or timeout. use pagination and limit size...

    """
    tree = {
        "id": path + str(level),
        "name": os.path.normpath(path).split(os.sep)[-1],
        "path": path,
        "folders": [],
        "musics": [],
    }
    for p in os.listdir(path):
        p_path = os.path.join(path, p)
        if os.path.isdir(p_path) and level > 1:
            tree["folders"].append(get_tree(p_path, level - 1))
        elif os.path.isfile(p_path) and os.path.splitext(p_path)[1] in AUDIO_EXTENSIONS:
            tree["musics"].append(
                {"name": p, "path": os.path.relpath(p_path, MUSIC_PATH)}
            )
    return tree


def get_tree_at(request, path=None):
    try:
        tree = get_tree(path if path else MUSIC_PATH, 2)
        # json_tree = json.dumps(tree, ensure_ascii=False)  # TODO check non-ASCII characters serialization
        return JsonResponse(tree)  # safe=False
    except Exception as e:
        return JsonResponse({"error": str(e)})
