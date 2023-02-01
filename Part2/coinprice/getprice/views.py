import os

from django.http import JsonResponse
import requests
import redis

# Create your views here.
CACHE_TTL = int(os.getenv("CACHE_TTL"))


def get_price(request):
    coin_id = request.GET.get('coin', os.getenv("COIN_NAME"))
    redis_client = redis.Redis(host=os.getenv("REDIS_URI"),
                               port=int(os.getenv("REDIS_PORT")))
    cached_value = redis_client.get(coin_id)
    if cached_value is not None:
        cached_value = float(cached_value.decode("utf-8"))
        print("reading from cache!",int(cached_value))
        return JsonResponse(data={coin_id: {"usd": cached_value}})

    response = requests.get(
        f'{os.getenv("API_URL")}?ids={coin_id}&vs_currencies=usd')
    value = response.json()[coin_id]["usd"]
    redis_client.set(coin_id, value, ex=CACHE_TTL)
    redis_client.save()
    return JsonResponse(response.json())
