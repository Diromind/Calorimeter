CREATE TABLE IF NOT EXISTS calorimeter.users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255),
    surname VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS calorimeter.records (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INT REFERENCES calorimeter.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    value INT NOT NULL
);

CREATE OR REPLACE FUNCTION calorimeter.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_records_updated_at ON calorimeter.records;

CREATE TRIGGER update_records_updated_at
BEFORE UPDATE ON calorimeter.records
FOR EACH ROW
EXECUTE FUNCTION calorimeter.update_timestamp();
