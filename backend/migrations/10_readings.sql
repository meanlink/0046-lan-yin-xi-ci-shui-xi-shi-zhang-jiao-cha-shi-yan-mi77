CREATE TABLE IF NOT EXISTS strip_readings (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 plate text NOT NULL REFERENCES plates(code),strip text NOT NULL,
 side text NOT NULL CHECK(side IN ('short','long')),
 temp numeric NOT NULL CHECK(temp BETWEEN 4 AND 70),
 density numeric NOT NULL CHECK(density BETWEEN 0 AND 2),
 fade numeric CHECK(fade BETWEEN 0 AND 1),
 state text NOT NULL DEFAULT 'active' CHECK(state IN ('active','discarded')),
 received_at timestamptz NOT NULL DEFAULT now(),
 CHECK((side='short' AND fade IS NULL) OR (side='long' AND fade IS NOT NULL))
);
-- 同一侧完全相同的读数只留一份；离线重传据此幂等，不新增试条。
CREATE UNIQUE INDEX IF NOT EXISTS strip_readings_exact ON strip_readings
 (plate,strip,side,temp,density,(COALESCE(fade,-1)));
CREATE INDEX IF NOT EXISTS strip_readings_lookup ON strip_readings(plate,strip,side,state);
