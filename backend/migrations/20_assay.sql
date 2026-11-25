CREATE TABLE IF NOT EXISTS assays (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, plate text NOT NULL REFERENCES plates(code),
 sample_key text NOT NULL,gain float NOT NULL,p float NOT NULL CHECK(p BETWEEN 0 AND 1),fade float NOT NULL,
 n int NOT NULL CHECK(n BETWEEN 6 AND 16),eligible bool NOT NULL
);
CREATE TABLE IF NOT EXISTS recipes (
 plate text PRIMARY KEY REFERENCES plates(code),assay bigint NOT NULL UNIQUE REFERENCES assays(id),
 wash_sec int NOT NULL,signer text NOT NULL,signed_at timestamptz NOT NULL DEFAULT now()
);
