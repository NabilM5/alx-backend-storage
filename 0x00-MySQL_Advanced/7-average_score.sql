-- Script to create ComputeAverageScoreForUser stored procedure
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN in_user_id INT)
BEGIN
    -- Declare a variable to hold the computed average
    DECLARE computed_avg DECIMAL(10, 2);

    -- Calculate the average score for the specified user
    SELECT AVG(score) INTO computed_avg
    FROM corrections
    WHERE user_id = in_user_id;

    -- Update the user's average_score in the users table
    UPDATE users
    SET average_score = IFNULL(computed_avg, 0)
    WHERE id = in_user_id;
END$$

DELIMITER ;
