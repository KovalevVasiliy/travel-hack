-- Table: public.gotorussia_travels_regions

-- DROP TABLE public.gotorussia_travels_regions;

BEGIN TRANSACTION;

CREATE SEQUENCE gotorussia_travels_regions_id_seq Start 1;

CREATE TABLE public.gotorussia_travels_regions
(
    id integer NOT NULL DEFAULT nextval('gotorussia_travels_regions_id_seq'::regclass),
    orig_id integer NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    slug character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    deleted_at timestamp(0) without time zone,
    territory_id integer,
    type_id integer,
    images text COLLATE pg_catalog."default",
    region_id integer,
    geo text COLLATE pg_catalog."default",
    local_id integer,
    intra_text text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    code character varying(255) COLLATE pg_catalog."default",
    json_info jsonb,
    points json,
    short_desc text COLLATE pg_catalog."default",
    map_points json,
    important boolean NOT NULL DEFAULT false,
    kogo character varying(50) COLLATE pg_catalog."default",
    komu character varying(50) COLLATE pg_catalog."default",
    tk_id integer,
    phone character varying(20) COLLATE pg_catalog."default",
    tpo_id integer,
    vinit character varying(50) COLLATE pg_catalog."default",
    variations jsonb,
    CONSTRAINT gotorussia_travels_regions_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gotorussia_travels_regions
    OWNER to "user";

GRANT ALL ON TABLE public.gotorussia_travels_regions TO "user";

-- Index: gotorussia_travels_regions_deleted_at_index

-- DROP INDEX public.gotorussia_travels_regions_deleted_at_index;

CREATE INDEX gotorussia_travels_regions_deleted_at_index
    ON public.gotorussia_travels_regions USING btree
    (deleted_at ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_regions_jsons_index

-- DROP INDEX public.gotorussia_travels_regions_jsons_index;

CREATE INDEX gotorussia_travels_regions_jsons_index
    ON public.gotorussia_travels_regions USING gin
    ((json_info -> 'counters'::text))
    TABLESPACE pg_default;
-- Index: gotorussia_travels_regions_name_index

-- DROP INDEX public.gotorussia_travels_regions_name_index;

CREATE INDEX gotorussia_travels_regions_name_index
    ON public.gotorussia_travels_regions USING btree
    (name)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_regions_origid_index

-- DROP INDEX public.gotorussia_travels_regions_origid_index;

CREATE UNIQUE INDEX gotorussia_travels_regions_origid_index
    ON public.gotorussia_travels_regions USING btree
    (orig_id DESC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_regions_slug_index

-- DROP INDEX public.gotorussia_travels_regions_slug_index;

CREATE UNIQUE INDEX gotorussia_travels_regions_slug_index
    ON public.gotorussia_travels_regions USING btree
    (slug)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_regions_tpo_id_uindex

-- DROP INDEX public.gotorussia_travels_regions_tpo_id_uindex;

CREATE UNIQUE INDEX gotorussia_travels_regions_tpo_id_uindex
    ON public.gotorussia_travels_regions USING btree
    (tpo_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_regions_typeid_idx

-- DROP INDEX public.gotorussia_travels_regions_typeid_idx;

CREATE INDEX gotorussia_travels_regions_typeid_idx
    ON public.gotorussia_travels_regions USING btree
    (type_id ASC NULLS LAST)
    TABLESPACE pg_default;

COMMIT;
