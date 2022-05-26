DO
$do$
BEGIN
    CREATE TABLE IF NOT EXISTS files_hash_record (
        task_id uuid,
        hash_value VARCHAR(200),
        hash_type VARCHAR(15) NOT NULL,
        status VARCHAR(15) NOT NULL,
        result VARCHAR(200) NOT NULL,
        PRIMARY KEY (task_id)
    );
END
$do$
