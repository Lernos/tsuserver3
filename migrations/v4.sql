PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS area(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT 
);

-- Populate area with old table 
INSERT INTO area(name) SELECT DISTINCT room_name from ic_events WHERE NOT EXISTS (SELECT NAME FROM AREA WHERE area.NAME = ic_events.room_name);

CREATE TABLE ic_events_new(
	event_time DATETIME DEFAULT CURRENT_TIMESTAMP,
	ipid INTEGER NOT NULL,
	area_id int,
	char_name TEXT,
	ic_name TEXT,
	message TEXT NOT NULL,
	FOREIGN KEY (ipid) REFERENCES ipids(ipid)
		ON DELETE CASCADE,
	FOREIGN KEY (area_id) REFERENCES area(id)
		ON DELETE CASCADE
);

-- Create New Table
INSERT INTO ic_events_new(event_time, ipid, area_id, char_name, ic_name, message) 
SELECT event_time, ipid, (select id from area where area.name = room_name) area_id, char_name, ic_name, message FROM ic_events;

drop table ic_events;
ALTER TABLE ic_events_new RENAME TO ic_events;


CREATE INDEX idx_event_ip ON ic_events (event_time, ipid);

VACUUM;

PRAGMA user_version = 4;