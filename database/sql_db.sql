create table if not exists users (
id integer primary key autoincrement,
username text unique,
password text not null
);

create table if not exists menu (
id integer primary key autoincrement,
title text unique,
url text not null
);