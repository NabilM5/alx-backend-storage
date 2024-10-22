#!/usr/bin/env python3
"""
Returns a list of students from the MongoDB collection,
ordered by their average score.

:param mongo_collection: pymongo collection object
:return: list of students with their average score added
"""

def top_students(mongo_collection):
    """
    Aggregates students' scores and calculates their average score.

    :param mongo_collection: pymongo collection object
    :return: list of students with their average score added
    """
    
    # Define the aggregation pipeline to calculate average scores
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
                "averageScore": -1  # Sort by averageScore in descending order
            }
        }
    ]

    # Execute the aggregation pipeline on the collection
    results = mongo_collection.aggregate(pipeline)

    # Convert results to a list and return
    return list(results)
