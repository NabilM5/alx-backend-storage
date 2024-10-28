#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable

redis_store = redis.Redis()
'''The module-level Redis instance.
'''

def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data and tracks request counts.'''
    @wraps(method)
    def invoker(url: str) -> str:
        '''The wrapper function for caching the output and tracking the request.'''
        
        # Increment count for the URL and ensure the count is correct
        if not redis_store.exists(f'count:{url}'):
            redis_store.set(f'count:{url}', 0)
        count_incremented = redis_store.incr(f'count:{url}')
        if count_incremented is None:
            return "Error: Count increment failed"
        
        # Check if there's a cached result
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        
        # Fetch and cache the result if not already cached
        result = method(url)
        
        # Set cache expiry for the result at 10 seconds
        redis_store.setex(f'result:{url}', 10, result)
        
        return result
    return invoker

@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
