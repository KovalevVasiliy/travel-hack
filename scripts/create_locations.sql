-- Table: public.gotorussia_travels_locations

-- DROP TABLE public.gotorussia_travels_locations;

BEGIN TRANSACTION;

CREATE SEQUENCE gotorussia_travels_locations_id_seq Start 1;

CREATE TABLE public.gotorussia_travels_locations
(
    id integer NOT NULL DEFAULT nextval('gotorussia_travels_locations_id_seq'::regclass),
    type_id jsonb,
    object_json jsonb,
    object_place character varying(255) COLLATE pg_catalog."default",
    object_description text COLLATE pg_catalog."default" NOT NULL,
    object_text text COLLATE pg_catalog."default",
    object_title character varying(255) COLLATE pg_catalog."default" NOT NULL,
    object_coord character varying(255) COLLATE pg_catalog."default",
    object_v_card text COLLATE pg_catalog."default",
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    slug character varying(255) COLLATE pg_catalog."default" NOT NULL,
    phone text COLLATE pg_catalog."default",
    alt_phones text COLLATE pg_catalog."default",
    adress text COLLATE pg_catalog."default",
    website text COLLATE pg_catalog."default",
    rt_id integer,
    images text COLLATE pg_catalog."default",
    group_id jsonb,
    local_id integer,
    area_id integer,
    region_id integer,
    district_id integer,
    moderated boolean,
    searchable tsvector,
    recommend boolean NOT NULL DEFAULT false,
    lat double precision DEFAULT 0,
    lon double precision DEFAULT 0,
    contacts jsonb,
    new_address text COLLATE pg_catalog."default",
    textstatus integer NOT NULL DEFAULT 0,
    address_info jsonb,
    ent boolean NOT NULL DEFAULT false,
    closed boolean DEFAULT false,
    rewritten boolean NOT NULL DEFAULT false,
    sort_order integer DEFAULT 1,
    CONSTRAINT gotorussia_travels_locations_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gotorussia_travels_locations
    OWNER to "user";

GRANT ALL ON TABLE public.gotorussia_travels_locations TO "user";
-- Index: gotorussia_travels_locations_areaid_index

-- DROP INDEX public.gotorussia_travels_locations_areaid_index;

CREATE INDEX gotorussia_travels_locations_areaid_index
    ON public.gotorussia_travels_locations USING btree
    (area_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_districtid_index

-- DROP INDEX public.gotorussia_travels_locations_districtid_index;

CREATE INDEX gotorussia_travels_locations_districtid_index
    ON public.gotorussia_travels_locations USING btree
    (district_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_ent_index

-- DROP INDEX public.gotorussia_travels_locations_ent_index;

CREATE INDEX gotorussia_travels_locations_ent_index
    ON public.gotorussia_travels_locations USING btree
    (ent ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_id_idx

-- DROP INDEX public.gotorussia_travels_locations_id_idx;

CREATE UNIQUE INDEX gotorussia_travels_locations_id_idx
    ON public.gotorussia_travels_locations USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_latlon_idx

-- DROP INDEX public.gotorussia_travels_locations_latlon_idx;

CREATE INDEX gotorussia_travels_locations_latlon_idx
    ON public.gotorussia_travels_locations USING btree
    (lat ASC NULLS LAST, lon ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_localid_index

-- DROP INDEX public.gotorussia_travels_locations_localid_index;

CREATE INDEX gotorussia_travels_locations_localid_index
    ON public.gotorussia_travels_locations USING btree
    (local_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_lonlat_idx

-- DROP INDEX public.gotorussia_travels_locations_lonlat_idx;

CREATE INDEX gotorussia_travels_locations_lonlat_idx
    ON public.gotorussia_travels_locations USING btree
    (lon ASC NULLS LAST, lat ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_regionid_index

-- DROP INDEX public.gotorussia_travels_locations_regionid_index;

CREATE INDEX gotorussia_travels_locations_regionid_index
    ON public.gotorussia_travels_locations USING btree
    (region_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_rtid_idx

-- DROP INDEX public.gotorussia_travels_locations_rtid_idx;

CREATE UNIQUE INDEX gotorussia_travels_locations_rtid_idx
    ON public.gotorussia_travels_locations USING btree
    (rt_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_slug_index

-- DROP INDEX public.gotorussia_travels_locations_slug_index;

CREATE UNIQUE INDEX gotorussia_travels_locations_slug_index
    ON public.gotorussia_travels_locations USING btree
    (slug)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_title_index

-- DROP INDEX public.gotorussia_travels_locations_title_index;

CREATE INDEX gotorussia_travels_locations_title_index
    ON public.gotorussia_travels_locations USING btree
    (object_title)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_locations_title_moderated_index

-- DROP INDEX public.gotorussia_travels_locations_title_moderated_index;

CREATE INDEX gotorussia_travels_locations_title_moderated_index
    ON public.gotorussia_travels_locations USING btree
    (object_title)
    TABLESPACE pg_default
    WHERE moderated IS TRUE;
-- Index: locations_searchable_index

-- DROP INDEX public.locations_searchable_index;

CREATE INDEX locations_searchable_index
    ON public.gotorussia_travels_locations USING gin
    (searchable)
    TABLESPACE pg_default;

COMMIT;
