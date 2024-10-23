#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable
import time


redis_store = redis.Redis(decode_responses=True)


def data_cacher(method: Callable[[str], str]) -> Callable[[str], str]:
    '''Decorator to cache the output of the fetched data.
    '''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output.
        Increments the access count for the given URL and caches its result.
        '''
        # Increment the count for the URL access
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result is not None:
            return result
        result = method(url)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Fetches the HTML content of a URL after caching the request's response,
    and tracks the request.
    '''
    return requests.get(url).text


if __name__ == "__main__":
    url = "http://google.com"
    print("First call (cache store):", get_page(url))
    print("Second call (cache hit):", get_page(url))
    time.sleep(11)
    print("Third call (cache expired):", get_page(url))
