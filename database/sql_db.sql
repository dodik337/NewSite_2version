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

create table if not exists profile (
id integer primary key autoincrement,
name text unique,
username text unique,
info text not null,
time integer not null
);