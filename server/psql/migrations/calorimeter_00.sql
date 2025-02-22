CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255),
    surname VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS records (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow';
    value INT NOT NULL
);

CREATE OR REPLACE FUNCTION updated_at_hook()
RETURNS TRIGGER AS $$
BEGIN
    NEW.update_at = NOW() AT TIME ZONE 'UTC' AT TIME ZONE 'Europe/Moscow';
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Create trigger to call the update_timestamp function before each update
CREATE TRIGGER updated_at_trigger
BEFORE UPDATE ON records
FOR EACH ROW
EXECUTE FUNCTION updated_at_hook();