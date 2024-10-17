-- Script to create the need_meeting view
DROP VIEW IF EXISTS need_meeting;  -- Drop the view if it already exists to avoid errors on creation

CREATE VIEW need_meeting AS
SELECT name
FROM students
WHERE score < 80
AND (last_meeting IS NULL OR last_meeting <= CURDATE() - INTERVAL 1 MONTH);
