DO $migrate$
DECLARE
    legacy boolean;
BEGIN
    SELECT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema='public' AND table_name='strips' AND column_name='short_temp'
    ) INTO legacy;
    IF legacy THEN
        -- 旧表把两侧读数挤在一行；改为只保留试条身份，两侧分存 strip_readings。
        CREATE TABLE IF NOT EXISTS strips_new (
            plate text REFERENCES plates(code),code text,
            state text NOT NULL DEFAULT 'incomplete'
                CHECK(state IN ('incomplete','pending','paired','excluded')),
            PRIMARY KEY (plate,code)
        );
        INSERT INTO strip_readings(plate,strip,side,temp,density,fade)
         SELECT plate,code,'short',short_temp,short_density,NULL FROM strips
         ON CONFLICT DO NOTHING;
        INSERT INTO strip_readings(plate,strip,side,temp,density,fade)
         SELECT plate,code,'long',long_temp,long_density,long_fade FROM strips
         ON CONFLICT DO NOTHING;
        INSERT INTO strips_new(plate,code,state)
         SELECT plate,code,
           CASE state WHEN 'paired' THEN 'paired' WHEN 'excluded' THEN 'excluded' ELSE 'pending' END
         FROM strips
         ON CONFLICT DO NOTHING;
        DROP TABLE strips;
        ALTER TABLE strips_new RENAME TO strips;
    ELSE
        CREATE TABLE IF NOT EXISTS strips (
            plate text REFERENCES plates(code),code text,
            state text NOT NULL DEFAULT 'incomplete'
                CHECK(state IN ('incomplete','pending','paired','excluded')),
            PRIMARY KEY (plate,code)
        );
    END IF;
END
$migrate$;
