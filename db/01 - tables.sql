CREATE SEQUENCE IF NOT EXISTS resource_types_ids AS INTEGER INCREMENT 1;
CREATE SEQUENCE IF NOT EXISTS resources_ids AS INTEGER INCREMENT 1;

CREATE TABLE resource_types (
    id INTEGER DEFAULT nextval('resource_types_ids'),
    name VARCHAR(100) NOT NULL,
    max_speed INTEGER NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE resources (
    id INTEGER DEFAULT nextval('resources_ids'),
    resource_type INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    cur_speed INTEGER NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT resource_type_fk FOREIGN KEY (resource_type) REFERENCES resource_types(id) ON DELETE RESTRICT ON UPDATE CASCADE
);