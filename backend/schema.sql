CREATE TABLE IF NOT EXISTS plates (
 code text PRIMARY KEY, negative text NOT NULL,paper text NOT NULL,short_sec int NOT NULL CHECK(short_sec>0),
 long_sec int NOT NULL CHECK(long_sec>short_sec),fade_limit numeric NOT NULL CHECK(fade_limit BETWEEN 0 AND 1),
 state text NOT NULL CHECK(state IN ('open','sealed'))
);
