#!/usr/bin/env python3
import uuid
import redis
from typing import Union, Optional
class Cache:
    def __init__(self):
        """Initialize the Cache class with a Redis client instance
        and flush the database."""
        self._redis = redis.Redis()
        self._redis.flushdb()
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the provided data in Redis using a randomly generated UUID key.
        :param data: The data to store in Redis. Can be of type str,
        bytes, int, or float.
        :return: The UUID key as a string under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
if __name__ == "__main__":
    cache = Cache()
    data = b"hello"
    key = cache.store(data)
    print(key)
    print(cache._redis.get(key))
