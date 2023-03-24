create table if not exists users (
id integer primary key autoincrement,
username text unique,
password text not null
);