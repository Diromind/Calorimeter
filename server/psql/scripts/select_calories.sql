SELECT * FROM calorimeter.records
WHERE user_id = $1 AND created_at::date = $2;