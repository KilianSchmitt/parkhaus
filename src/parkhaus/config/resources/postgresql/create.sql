-- Copyright (C) 2022 - present Juergen Zimmermann, Hochschule Karlsruhe
--
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU General Public License as published by
-- the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU General Public License for more details.
--
-- You should have received a copy of the GNU General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.

-- TEXT statt varchar(n):
-- "There is no performance difference among these three types, apart from a few extra CPU cycles
-- to check the length when storing into a length-constrained column"
-- ggf. CHECK(char_length(nachname) <= 255)

-- https://www.postgresql.org/docs/current/manage-ag-tablespaces.html
SET default_tablespace = parkhausspace;

-- https://www.postgresql.org/docs/current/sql-createtable.html
-- https://www.postgresql.org/docs/current/datatype.html
-- https://www.postgresql.org/docs/current/sql-createtype.html
-- https://www.postgresql.org/docs/current/datatype-enum.html
CREATE TYPE kundentyp AS ENUM ('PREMIUM', 'BASIS', 'ANWOHNER');

CREATE TABLE IF NOT EXISTS patient (
    id            INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version       INTEGER NOT NULL DEFAULT 0,
    name          TEXT NOT NULL,
    kapazitaet    INTEGER NOT NULL CHECK (kapazitaet >= 0),
    tarif_pro_stunde NUMERIC(10,2) NOT NULL,
    erzeugt       TIMESTAMP NOT NULL,
    aktualisiert  TIMESTAMP NOT NULL
);

-- default: btree
CREATE INDEX IF NOT EXISTS parkhaus_name_idx ON parkhaus(name);

CREATE TABLE IF NOT EXISTS adresse (
    id          INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    plz         TEXT NOT NULL CHECK (plz ~ '\d{5}'),
    ort         TEXT NOT NULL,
    strasse     TEXT NOT NULL,
    hausnummer  TEXT NOT NULL,
    parkhaus_id INTEGER NOT NULL REFERENCES parkhaus ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS adresse_parkhaus_id_idx ON adresse(parkhaus_id);
CREATE INDEX IF NOT EXISTS adresse_plz_idx ON adresse(plz);

CREATE TABLE IF NOT EXISTS auto (
    id          INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    kennzeichen TEXT NOT NULL,
    einfahrtszeit TIMESTAMP NOT NULL,
    kundentyp kundentyp NOT NULL,
    parkhaus_id INTEGER NOT NULL REFERENCES parkhaus ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS auto_parkhaus_id_idx ON auto(parkhaus_id);
