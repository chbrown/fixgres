-- run like
-- $ dropdb fixgres; createdb fixgres && psql fixgres < schema.sql
CREATE TABLE emails (
    id serial PRIMARY KEY,
    domain text NOT NULL,
    
    header_from text,
    header_to text NOT NULL,
    header_subject text,
    header_date timestamp,
      
    postgres_filename text,
    original text,

    created timestamp DEFAULT current_timestamp NOT NULL,
    archived timestamp,
    tags text
);
