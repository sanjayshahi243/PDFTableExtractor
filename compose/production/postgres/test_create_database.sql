DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = 'fam_db') THEN
      RAISE NOTICE 'Database already exists';  -- optional
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()  -- current db
                        , 'CREATE DATABASE fam_db');
   END IF;
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'fam_user') THEN

      RAISE NOTICE 'Role "fam_user" already exists. Skipping.';
   ELSE
      CREATE USER fam_user with password 'EsozkG%K7HG8VL';
      GRANT ALL PRIVILEGES ON DATABASE fam_db TO fam_user;
   END IF;
END
$do$;
