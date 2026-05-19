# Query to find the top 10 companies with the most electric vehicles registered
SELECT
	s.make AS 'Company_Name',
    COUNT(f.dol_vehicle_id) AS 
'Total_EVs_Registered'
FROM
    fact_ev_registrations f 
JOIN
    dim_vehicle_specs s ON f.vehicle_id = s.vehicle_id
GROUP BY
    s.make
ORDER BY
	Total_EVs_Registered DESC
LIMIT 10;

# Query to find the top 10 cities with the most electric vehicles registered
SELECT
	l.city AS 'City_Name',
    COUNT(f.dol_vehicle_id) AS
'Total_EVs'
FROM
	fact_ev_Registrations f
JOIN
	dim_location l ON f.location_id = l.location_id
GROUP BY
	l.city
ORDER BY
	Total_EVs DESC
LIMIT 10;

# Analyze market preference between Battery Electric Vehicles (BEV) and Plug-in Hybrid Electric Vehicles (PHEV)
SELECT
	s.ev_type AS 'EV_Type',
    COUNT(f.dol_vehicle_id) AS
'Total_Vehicles'
FROM
	fact_ev_registrations f
JOIN
	dim_vehicle_specs s ON
f.vehicle_id = s.vehicle_id
GROUP BY
	s.ev_type
ORDER BY
	Total_Vehicles DESC;

# Analyze the trend of electric vehicle registrations over the years
SELECT
	model_year AS 'Year',
    COUNT(dol_vehicle_id) AS
'Total_EVs'
FROM
	fact_ev_registrations
WHERE
	model_year >= 2010
GROUP BY
	model_year
ORDER BY
	Year DESC;

# Analyze the average electric range of vehicles by company
SELECT
	s.make AS 'Company_Name',
    ROUND(AVG(f.electric_range), 2)
AS 'Avg_Electric_Range'
FROM
	fact_ev_registrations f
JOIN
	dim_vehicle_specs s ON
f.vehicle_id = s.vehicle_id
WHERE
	f.electric_range > 0    
GROUP BY
	s.make
ORDER BY
	Avg_Electric_Range DESC
LIMIT 10;