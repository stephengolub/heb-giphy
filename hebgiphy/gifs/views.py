import json

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET
from django.http import JsonResponse

from hebgiphy.gifs.giphy import GIPHY_API
from hebgiphy.gifs import models


@login_required
@require_GET
def gif_search(request):
    """Search GIPHY for a Gif with specified criteria.

    Arguments:
        request (django.http.request.HttpRequest): The incoming request object.

    Returns:
        django.http.JsonResponse: The response data.
    """
    queryparams = request.GET.dict()
    q = queryparams.pop('q')
    queryparams['offset'] = int(queryparams.pop('offset', 0))
    queryparams['limit'] = int(queryparams.pop('limit', 25))
    queryparams['rating'] = queryparams.pop('rating', 'g')
    result = GIPHY_API.gifs_search_get(q, **queryparams).to_dict()
    data = {d['id']: models.Gif.get_dict_from_giphy(d) for d in result['data']}
    stored_gifs = models.Gif.objects.filter(giphy_id__in=data.keys())
    for g in stored_gifs:
        data[g.giphy_id]['giphy_tags'] = [t.as_dict() for t in g.tags.all()]
    result['data'] = list(data.values())
    return JsonResponse(result)


@login_required
@require_http_methods(["POST", "DELETE"])
def gif_favorite(request, giphy_id):
    """Favorite a specific Gif

    Arguments:
        request (django.http.request.HttpRequest): The incoming request object.
        giphy_id (str): The ID String that GIPHY uses.

    Returns:
        django.http.JsonResponse: The response data.
    """
    try:
        model = models.Gif.objects.get(giphy_id=giphy_id)
    except models.Gif.DoesNotExist:
        model = None
    if request.method == 'POST':
        if model is None:
            result = GIPHY_API.gifs_gif_id_get(giphy_id)
            model = models.Gif.from_giphy_response(result.data)
        model.favorited_by.add(request.user)
        model.save()
        return JsonResponse(model.as_dict())
    elif request.method == 'DELETE':
        if model is None:
            return JsonResponse({
                'status': 'Not Favorited',
                'giphy_id': giphy_id,
            })
        model.delete()
        return JsonResponse({
            'status': 'success',
            'giphy_id': giphy_id,
        })


@login_required
@require_http_methods(["GET", "POST"])
def gif_tags(request, giphy_id):
    """Get or store tags on a Gif

    Arguments:
        request (django.http.request.HttpRequest): The incoming request object.
        giphy_id (str): The ID String that GIPHY uses.

    Returns:
        django.http.JsonResponse: The response data.
    """
    model = models.Gif.objects.get(giphy_id=giphy_id)
    if request.method == 'GET':
        return JsonResponse(model.as_dict())

    tag_source, tag_source_created = models.TagSource.objects.get_or_create(name='user')
    tagList = json.loads(request.body)
    tags = [models.Tag.objects.get_or_create(name=t, source=tag_source)[0] for t in tagList]
    model.tags.set(tags)
    return JsonResponse(model.as_dict())


@login_required
@require_GET
def gif_favorite_list(request):
    """Get list of favorite gifs.

    Arguments:
        request (django.http.request.HttpRequest): The incoming request object.

    Returns:
        django.http.JsonResponse: The response data.
    """
    gifs = request.user.gif_set.all()
    return JsonResponse([gif.as_dict() for gif in gifs], safe=False)
