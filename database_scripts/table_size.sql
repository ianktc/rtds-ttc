SELECT 
  name,
  SUM(pgsize) AS size_bytes
FROM dbstat
WHERE name = 'vehicle_positions'
GROUP BY name;
