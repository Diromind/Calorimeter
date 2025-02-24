ALTER TABLE calorimeter.records
ADD COLUMN description TEXT;

CREATE INDEX IF NOT EXISTS idx_telegram_id ON calorimeter.users (telegram_id);
