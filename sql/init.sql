BEGIN;

CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    repo VARCHAR(255) NOT NULL,
    owner VARCHAR(255) NOT NULL,
    position_cur INTEGER,
    position_prev INTEGER,
    stars INTEGER,
    watchers INTEGER,
    forks INTEGER,
    open_issues INTEGER,
    "language" VARCHAR(50),

    UNIQUE(repo)
);

# TODO: create indexes