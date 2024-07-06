import os
from django.http import JsonResponse
from ..models import Music, MusicSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
import json
from ..tasks import parse_filesystem
from ..consts import MUSIC_PATH, AUDIO_EXTENSIONS
from ..services.filesystem import updateDb


def get_tree(path, level):
    """
    edge cases :
        * Not handling hidden files / folders
        * Not following symlinks (os.scandir)
        * Large directories may cause out of memory or timeout. use pagination and limit size...

    """
    tree = {
        "name": os.path.normpath(path).split(os.sep)[-1],
        "path": path,
        "folders": [],
        "musics": [],
        "opened": False,
    }
    for p in os.listdir(path):
        p_path = os.path.join(path, p)
        if level > 0:
            if os.path.isdir(p_path):
                tree["folders"].append(get_tree(p_path, level - 1))
            elif (
                os.path.isfile(p_path)
                and os.path.splitext(p_path)[1] in AUDIO_EXTENSIONS
            ):
                existing_music = Music.objects.filter(path=p_path)
                if not existing_music:
                    music_result = updateDb(p, p_path)
                else:
                    music_result = {"music": existing_music.first()}
                if music_result["music"]:
                    music_dict = MusicSerializer(music_result["music"]).data
                    music_result["music"] = music_dict
                tree["musics"].append(music_result)
    return tree


# TODO endpoint for scanning in background


class FolderView(APIView):
    def post(self, request):
        try:
            path = None
            if request.body:
                body = json.loads(request.body)
                path = body["path"]
            tree = get_tree(path if path else MUSIC_PATH, 1)
            # json_tree = json.dumps(tree, ensure_ascii=False)  # TODO check non-ASCII characters serialization
            return JsonResponse(tree)  # safe=False
        except Exception as e:
            return JsonResponse({"error": str(e)})


@api_view(["GET"])
def refresh_library(request):
    force = request.query_params.get("force", "False")
    result = parse_filesystem.delay(force.lower() == "true")
    return JsonResponse({"result": result.task_id})
