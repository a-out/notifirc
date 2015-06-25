CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    matches TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE filters (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    args TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE match_filters (
    match_id INT REFERENCES matches (id) ON UPDATE CASCADE ON DELETE CASCADE,
    filter_id INT REFERENCES filters (id) ON UPDATE CASCADE,
    CONSTRAINT match_filters_pkey PRIMARY KEY (match_id, filter_id)
);
