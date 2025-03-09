CREATE TABLE IF NOT EXISTS calorimeter.places (
    item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_id INT NOT NULL,
    item_name VARCHAR(255) NOT NULL,
    place_name VARCHAR(255) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_places_place_id
ON calorimeter.places (place_id);

ALTER TABLE calorimeter.records
ADD COLUMN item_uuid UUID;

ALTER TABLE calorimeter.records
ADD CONSTRAINT fk_records_places_item_uuid
FOREIGN KEY (item_uuid) REFERENCES calorimeter.places(item_id)
ON DELETE SET NULL;

CREATE TYPE calorimeter.stat AS (
    records_count INT,
    total_value INT
);

CREATE TABLE calorimeter.weekly_stats (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL REFERENCES calorimeter.users(telegram_id),
    first_day_of_period DATE NOT NULL,
    stat calorimeter.stat NOT NULL
);