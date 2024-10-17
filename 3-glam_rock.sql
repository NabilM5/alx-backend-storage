-- SQL script to find Glam rock bands and rank them by longevity
SELECT
    band_name,
    -- Calculate lifespan: If `split` is NULL, use 2022; otherwise, use the `split` year
    IFNULL(split, 2022) - formed AS lifespan
FROM
    metal_bands
WHERE
    style LIKE '%Glam rock%' -- Filter bands by style containing 'Glam rock'
ORDER BY
    lifespan DESC; -- Order by lifespan in descending order
