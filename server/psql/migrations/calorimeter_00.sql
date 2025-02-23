CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS calorimeter.users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255),
    surname VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS calorimeter.records (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow',
    value INT NOT NULL
);

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_at = CURRENT_TIMESTAMP AT TIME ZONE 'Europe/Moscow';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Create trigger to call the update_timestamp function before each update
CREATE TRIGGER update_records_updated_at
BEFORE UPDATE ON records
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();