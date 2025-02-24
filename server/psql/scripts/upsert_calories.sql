INSERT INTO calorimeter.records (uuid, user_id, value)
VALUES ($1, $2, $3)
ON CONFLICT (uuid)
DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP;