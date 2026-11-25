CREATE TABLE IF NOT EXISTS strips (
 plate text REFERENCES plates(code),code text,short_temp numeric NOT NULL,long_temp numeric NOT NULL,
 short_density numeric NOT NULL CHECK(short_density BETWEEN 0 AND 2),long_density numeric NOT NULL CHECK(long_density BETWEEN 0 AND 2),
 long_fade numeric NOT NULL CHECK(long_fade BETWEEN 0 AND 1),
 state text NOT NULL DEFAULT 'pending' CHECK(state IN ('pending','paired','excluded')), PRIMARY KEY (plate,code)
);
