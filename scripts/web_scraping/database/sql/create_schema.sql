CREATE SCHEMA boticarios_transactional AUTHORIZATION hseq_admin;

GRANT ALL ON SCHEMA boticarios_transactional TO cloudsqlsuperuser WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES IN SCHEMA boticarios_transactional
GRANT ALL ON TABLES TO cloudsqlsuperuser WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES IN SCHEMA boticarios_transactional
GRANT ALL ON SEQUENCES TO cloudsqlsuperuser WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES IN SCHEMA boticarios_transactional
GRANT EXECUTE ON FUNCTIONS TO cloudsqlsuperuser WITH GRANT OPTION;

ALTER DEFAULT PRIVILEGES IN SCHEMA boticarios_transactional
GRANT USAGE ON TYPES TO cloudsqlsuperuser WITH GRANT OPTION;