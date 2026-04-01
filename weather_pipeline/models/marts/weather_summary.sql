SELECT
    city,
    country,
    ROUND(AVG(temperature_c)::numeric, 2)  AS avg_temp_c,
    ROUND(MAX(temperature_c)::numeric, 2)  AS max_temp_c,
    ROUND(MIN(temperature_c)::numeric, 2)  AS min_temp_c,
    ROUND(AVG(humidity_pct)::numeric, 2)   AS avg_humidity_pct,
    ROUND(AVG(wind_speed_ms)::numeric, 2)  AS avg_wind_speed_ms,
    COUNT(*)                               AS total_readings
FROM {{ ref('stg_weather') }}
GROUP BY city, country