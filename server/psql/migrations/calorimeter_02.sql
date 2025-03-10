CREATE TABLE IF NOT EXISTS calorimeter.places (
    place_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    place_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS calorimeter.items (
    item_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    item_name VARCHAR(255),
    place_id UUID REFERENCES calorimeter.places(place_id),
    calories FLOAT NOT NULL,
    proteins FLOAT,
    fats FLOAT,
    carbs FLOAT
);

CREATE INDEX IF NOT EXISTS idx_places_place_id
ON calorimeter.places (place_id);

ALTER TABLE calorimeter.records
ADD COLUMN item_uuid UUID NOT NULL;

ALTER TABLE calorimeter.records
ADD CONSTRAINT fk_records_places_item_uuid
FOREIGN KEY (item_uuid) REFERENCES calorimeter.items(item_id)
ON DELETE SET NULL;

ALTER TABLE calorimeter.records
ALTER COLUMN user_id SET NOT NULL,
ALTER COLUMN created_at SET NOT NULL,
ALTER COLUMN updated_at SET NOT NULL;

CREATE TYPE calorimeter.stat AS (
    records_count INT,
    total_value INT
);

CREATE TABLE calorimeter.statistics (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT NOT NULL REFERENCES calorimeter.users(telegram_id),
    first_day_of_period DATE NOT NULL,
    stat calorimeter.stat NOT NULL
);