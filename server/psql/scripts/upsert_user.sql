INSERT INTO calorimeter.users (telegram_id, name, surname)
VALUES ($1, $2, $3)
ON CONFLICT (telegram_id)
DO UPDATE SET name = EXCLUDED.name, surname = EXCLUDED.surname;