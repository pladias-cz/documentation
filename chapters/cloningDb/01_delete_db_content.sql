-- CAREFULLY !!!!! --- !!!! --- !!!! ---
TRUNCATE TABLE biblio.bibliography  CASCADE;
TRUNCATE TABLE measurements.sections  CASCADE;
TRUNCATE TABLE measurements.data_unmeasurable  CASCADE;
TRUNCATE TABLE measurements.enumerates  CASCADE;

DROP VIEW IF EXISTS measurements.dana_features;
DROP VIEW IF EXISTS measurements.milanova_tabulka;
DROP VIEW IF EXISTS measurements.enumerates_features_overview;
DROP VIEW IF EXISTS measurements.traits_including_taxon;
DROP VIEW IF EXISTS measurements.dana_enumerates;
DROP VIEW IF EXISTS measurements.dana_sections;
DROP VIEW IF EXISTS measurements.dana_traits;

TRUNCATE TABLE public.taxons  CASCADE;
TRUNCATE TABLE public.users  CASCADE;
TRUNCATE TABLE public.syntaxons  CASCADE;
TRUNCATE TABLE public.taxons_history  CASCADE;
TRUNCATE TABLE public.temporary_files  CASCADE;
TRUNCATE TABLE public.downloads  CASCADE;
TRUNCATE TABLE public.institutions  CASCADE;

TRUNCATE TABLE atlas.csv_map_details  CASCADE;
TRUNCATE TABLE atlas.pdf_map  CASCADE;
TRUNCATE TABLE  atlas.authors CASCADE;
TRUNCATE TABLE  atlas.herbariums CASCADE;
TRUNCATE TABLE  atlas.projects CASCADE;

DROP VIEW IF EXISTS atlas."danihelkaNDOP";
DROP VIEW IF EXISTS atlas."tempKaplanAuthorscleaningSmejdova" ;
DROP VIEW IF EXISTS atlas."kaplanAuthorsAndRecordCountsRecordsID" ;
DROP VIEW IF EXISTS atlas."kaplanAuthorsAndRecordCounts" ;
DROP VIEW IF EXISTS atlas."kaplanComments" ;
DROP VIEW IF EXISTS atlas."kaplan_importedauthors_users" ;
DROP VIEW IF EXISTS atlas."records_source_distinct" ;
DROP VIEW IF EXISTS atlas."wildGrid2" ;
DROP VIEW IF EXISTS atlas."wildGrid3" ;
DROP VIEW IF EXISTS atlas."wildGrid4";
DROP VIEW IF EXISTS atlas."wildGrid5" ;


DROP TABLE IF EXISTS public_web.images;
DROP TABLE IF EXISTS public_web.vegetation_images;
DROP TABLE IF EXISTS public_web.boolean_features_translate  ;
DROP TABLE IF EXISTS public_web.countries;
DROP TABLE IF EXISTS public_web.downloads_files;
DROP TABLE IF EXISTS public_web.downloads  ;
DROP TABLE IF EXISTS public_web.kvetena  ;
DROP TABLE IF EXISTS public_web.rel_syntaxons_sections  ;
DROP TABLE IF EXISTS public_web.syntaxons_sections  ;
DROP TABLE IF EXISTS public_web.syntaxons_taxons;
DROP TABLE IF EXISTS public_web.vegkey;
DROP SEQUENCE public_web.images_clopla_id_seq;
DROP MATERIALIZED VIEW public_web.m_traits_including_taxon_withhacks;

REFRESH MATERIALIZED VIEW public_web.m_plants_distribution;

REFRESH MATERIALIZED VIEW measurements.m_occurrence_frequency;
REFRESH MATERIALIZED VIEW public.m_descendant_taxons;

DROP SCHEMA atlas_nonvascular CASCADE;
DROP SCHEMA bayernflora  CASCADE;

DROP TABLE geodata."quadrants_AOPK";
DROP TABLE geodata.quadrants_deprecated;
DROP TABLE geodata.regions;
DROP TABLE geodata."squares_AOPK";
DROP TABLE geodata.squares_deprecated;
TRUNCATE TABLE  measurements.trait_export_snapshots;
TRUNCATE TABLE  public.publications CASCADE ;


-- --kontrola tabulek které zůstaly plné
-- SELECT schemaname,relname,n_live_tup
-- FROM pg_stat_user_tables
-- WHERE n_live_tup >0
-- ORDER BY schemaname, n_live_tup DESC;

-- ještě je potřeba přenastavit hodnoty skoro všech sekvencí tak, aby byl v budoucnu možný jednoduchý join mezi českou a slovenskou verzí

ALTER SEQUENCE atlas.authors_id_seq RESTART WITH 200000;
ALTER SEQUENCE atlas.batch_id_seq RESTART WITH 1;
ALTER SEQUENCE atlas.comments_id_seq RESTART WITH 1;
ALTER SEQUENCE atlas.csv_map_details_id_seq RESTART WITH 1;
ALTER SEQUENCE atlas.excel_id_seq RESTART WITH 1;
ALTER SEQUENCE atlas.herbariums_id_seq RESTART WITH 200000;
ALTER SEQUENCE atlas.pdf_map_taxon_id_seq RESTART WITH 1;
ALTER SEQUENCE atlas.projects_id_seq RESTART WITH 20000;
ALTER SEQUENCE atlas.records_history_id_seq RESTART WITH 1000000000;
ALTER SEQUENCE atlas.records_id_seq RESTART WITH 1000000000;
ALTER SEQUENCE biblio.bibliography_id_seq RESTART WITH 200000;
ALTER SEQUENCE measurements.enumerates_id_seq RESTART WITH 200000;
ALTER SEQUENCE measurements.enumerates__values_id_seq RESTART WITH 200000;
ALTER SEQUENCE measurements.features_id_seq RESTART WITH 200000;
ALTER SEQUENCE measurements.sections_id_seq RESTART WITH 20000;
ALTER SEQUENCE measurements.traits_id_seq RESTART WITH 200000;
ALTER SEQUENCE public.syntaxons_id_seq RESTART WITH 200000;
ALTER SEQUENCE public.taxons_backup_version_summary_id_seq RESTART WITH 1;
ALTER SEQUENCE public.taxons_history_id_seq RESTART WITH 1;
ALTER SEQUENCE public.taxons_id_seq RESTART WITH 200000;
ALTER SEQUENCE public.temporary_files_id_seq RESTART WITH 1;
ALTER SEQUENCE public.users_activity_log_id_seq RESTART WITH 1;
ALTER SEQUENCE public.users_id_seq RESTART WITH 20000;

ALTER SEQUENCE geodata.phytochorions_rowid_seq RESTART WITH 1000;
ALTER SEQUENCE geodata.phytochorions_outside_cz_rowid_seq RESTART WITH 1000;
ALTER SEQUENCE measurements.data_enum_id_seq RESTART WITH 1;
ALTER SEQUENCE measurements.data_integer_id_seq RESTART WITH 1;
ALTER SEQUENCE measurements.data_occurrence_frequency_id_seq RESTART WITH 1;
ALTER SEQUENCE measurements.data_real_multi_id_seq RESTART WITH 1;
ALTER SEQUENCE measurements.data_year_id_seq RESTART WITH 1;
ALTER SEQUENCE measurements.trait_export_snapshots_id_seq RESTART WITH 1;
ALTER SEQUENCE public.publications_id_seq RESTART WITH 1;
ALTER SEQUENCE public.synonyms_id_seq RESTART WITH 1;


-- -- kontrola sekvencí
-- select schemaname, sequencename, start_value, last_value from pg_sequences
-- WHERE last_value is not null AND last_value >1
-- ORDER BY schemaname, sequencename;

-- heslo je "cibule"
INSERT INTO users VALUES (DEFAULT, 'dusan.senko@savba.sk', 'oGReJi/HMQE=', 'Dušan', 'Senko', NULL, true, true, false, NULL, true, true, true, true, NULL);

INSERT INTO public.institutions VALUES ('BU', 'Botanický ústav AV SK, v. v. i.', 'BÚ AV SK', 'Institute of Botany, The Slovakia Academy of Sciences');

INSERT INTO atlas.projects VALUES (DEFAULT , 'Osobní nálezová databáze', 'Osobní nálezy', 'BU', 100 , 'Database of personal records');
INSERT INTO atlas.projects VALUES (DEFAULT , 'Fytocenologická data ', 'BU', 'BU', 50 , 'Institute of botany');