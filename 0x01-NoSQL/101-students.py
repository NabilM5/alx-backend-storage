#!/usr/bin/env python3
"""
    Returns all students from the collection
    ordered by average score.

    :param mongo_collection: pymongo collection object
    :return: list of students with their average score added
"""


def top_students(mongo_collection):
    pipeline = [
        {
            "$addFields": {
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    results = mongo_collection.aggregate(pipeline)
    return list(results)
