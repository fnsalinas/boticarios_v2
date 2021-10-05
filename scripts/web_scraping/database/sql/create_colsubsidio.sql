-- Borrar la tabla
DROP TABLE IF EXISTS boticarios_transactional.colsubsidio;

-- Crear tabla de colsubsidio
CREATE TABLE IF NOT EXISTS boticarios_transactional.colsubsidio (
	id						SERIAL,
	product_url				TEXT,
	category_url			TEXT,
	scraping_date			DATE,
	scraping_time			TIME,
	title					TEXT,
	presentation			TEXT,
	full_price				NUMERIC,
	final_price				NUMERIC,
	datetime_created		TIMESTAMP without TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT pk_colsubsidio PRIMARY KEY (id)
);

ALTER TABLE boticarios_transactional.colsubsidio OWNER to postgres;

GRANT ALL ON TABLE boticarios_transactional.colsubsidio TO cloudsqlsuperuser WITH GRANT OPTION;