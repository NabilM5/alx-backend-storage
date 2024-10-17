-- Script to create ComputeAverageWeightedScoreForUsers stored procedure
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Temporary table to store intermediate results
    CREATE TEMPORARY TABLE IF NOT EXISTS WeightedScores (
        user_id INT,
        total_weighted_score FLOAT,
        total_weight INT
    );

    -- Clear the temporary table
    TRUNCATE TABLE WeightedScores;

    -- Calculate total weighted scores and total weights for each user
    INSERT INTO WeightedScores (user_id, total_weighted_score, total_weight)
    SELECT 
        c.user_id,
        SUM(c.score * p.weight) AS total_weighted_score,
        SUM(p.weight) AS total_weight
    FROM 
        corrections c
    INNER JOIN 
        projects p ON c.project_id = p.id
    GROUP BY 
        c.user_id;

    -- Update users' average scores based on weighted scores
    UPDATE 
        users u
    JOIN 
        WeightedScores ws ON u.id = ws.user_id
    SET 
        u.average_score = CASE
            WHEN ws.total_weight > 0 THEN ws.total_weighted_score / ws.total_weight
            ELSE 0
        END;

    -- Clean up temporary table
    DROP TEMPORARY TABLE IF EXISTS WeightedScores;
END$$

DELIMITER ;
