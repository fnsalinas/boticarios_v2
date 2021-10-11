-- Borrar la tabla
DROP TABLE IF EXISTS boticarios_transactional.cafam;

-- Crear tabla de colsubsidio
CREATE TABLE IF NOT EXISTS boticarios_transactional.cafam (
	id						SERIAL,
	product_url				TEXT,
	category_url			TEXT,
	scraping_date			DATE,
	scraping_time			TIME,
	title					TEXT,
	productBrand			TEXT,
	full_price				NUMERIC,
	final_price				NUMERIC,
	datetime_created		TIMESTAMP without TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT pk_cafam PRIMARY KEY (id)
);

ALTER TABLE boticarios_transactional.cafam OWNER to hseq_admin;

GRANT ALL ON TABLE boticarios_transactional.cafam TO cloudsqlsuperuser WITH GRANT OPTION;