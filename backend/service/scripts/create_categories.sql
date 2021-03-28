-- Table: public.gotorussia_types_category

-- DROP TABLE public.gotorussia_types_category;

BEGIN TRANSACTION;

CREATE SEQUENCE gotorussia_types_category_id_seq Start 1;

CREATE TABLE public.gotorussia_types_category
(
    id integer NOT NULL DEFAULT nextval('gotorussia_types_category_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    has_child boolean NOT NULL DEFAULT false,
    is_child boolean NOT NULL DEFAULT false,
    childrens json,
    parents json,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    slug text COLLATE pg_catalog."default",
    meta_title character varying COLLATE pg_catalog."default",
    meta_description character varying COLLATE pg_catalog."default",
    meta_keywords character varying COLLATE pg_catalog."default",
    canonical_url character varying COLLATE pg_catalog."default",
    redirect_url character varying COLLATE pg_catalog."default",
    CONSTRAINT gotorussia_types_category_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gotorussia_types_category
    OWNER to "user";

GRANT ALL ON TABLE public.gotorussia_types_category TO "user";

COMMIT;
