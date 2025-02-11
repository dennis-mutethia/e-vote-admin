CREATE TABLE IF NOT EXISTS counties (
  id TEXT PRIMARY KEY,
  code TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT
);

CREATE TABLE IF NOT EXISTS constituencies (
  id TEXT PRIMARY KEY,
  code TEXT,
  county_id TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT
);

CREATE TABLE IF NOT EXISTS wards (
  id TEXT PRIMARY KEY,
  code TEXT,
  constituency_id TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT
);

CREATE TABLE IF NOT EXISTS polling_stations (
  id TEXT PRIMARY KEY,
  code TEXT,
  ward_id TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT
);

CREATE TABLE IF NOT EXISTS voters (
  id TEXT,
  id_number TEXT,
  fingerprint_hash TEXT,
  first_name TEXT,
  last_name TEXT,
  other_name TEXT,
  phone TEXT,
  polling_station_id TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  PRIMARY KEY (id_number, polling_station_id)
) PARTITION BY LIST (polling_station_id);

CREATE TABLE IF NOT EXISTS sms_codes (
  id TEXT,
  voter_id TEXT,
  code TEXT,
  polling_station_id TEXT,
  status INT DEFAULT 0,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  PRIMARY KEY (id, polling_station_id)
) PARTITION BY LIST (polling_station_id);

CREATE TABLE IF NOT EXISTS elections (
  id TEXT PRIMARY KEY,
  code TEXT,
  name TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT
);

CREATE TABLE IF NOT EXISTS parties (
  id TEXT PRIMARY KEY,
  name TEXT,
  icon TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT
);

CREATE TABLE IF NOT EXISTS candidates (
  id TEXT PRIMARY KEY,
  voter_id TEXT,
  party_id TEXT,
  icon TEXT,
  running_mate_voter_id TEXT,
  running_mate_icon TEXT,
  election_id TEXT,
  unit TEXT,
  unit_id TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  UNIQUE (voter_id)
);

CREATE TABLE IF NOT EXISTS votes (
  election_id TEXT,
  candidate_id TEXT,
  voter_id TEXT,
  polling_station_id TEXT,
  ward_id TEXT,
  constituency_id TEXT,
  county_id TEXT,
  created_at TIMESTAMP,
  created_by TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by TEXT,
  PRIMARY KEY (election_id, candidate_id, voter_id, polling_station_id)
) PARTITION BY LIST (polling_station_id);

