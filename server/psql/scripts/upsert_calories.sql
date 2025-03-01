INSERT INTO calorimeter.records (uuid, user_id, value, description)
VALUES ($1, $2, $3, $4)
ON CONFLICT (uuid)
DO UPDATE SET value = EXCLUDED.value, updated_at = CURRENT_TIMESTAMP;