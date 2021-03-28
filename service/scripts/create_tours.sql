-- Table: public.gotorussia_travels_tours

-- DROP TABLE public.gotorussia_travels_tours;

CREATE SEQUENCE gotorussia_travels_tours_id_seq Start 1;

CREATE TABLE public.gotorussia_travels_tours
(
    id integer NOT NULL DEFAULT nextval('gotorussia_travels_tours_id_seq'::regclass),
    tour_description text COLLATE pg_catalog."default" NOT NULL,
    tour_text text COLLATE pg_catalog."default",
    tour_title character varying(255) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    slug character varying(255) COLLATE pg_catalog."default",
    phone text COLLATE pg_catalog."default",
    address text COLLATE pg_catalog."default",
    website character varying(255) COLLATE pg_catalog."default",
    local_id integer,
    area_id integer,
    region_id integer,
    district_id integer,
    moderated boolean NOT NULL DEFAULT false,
    recommend boolean NOT NULL DEFAULT false,
    lat double precision,
    lon double precision,
    contacts jsonb,
    sort_order integer NOT NULL DEFAULT 1,
    tour_json jsonb,
    category_id integer NOT NULL DEFAULT 1,
    rewritten boolean NOT NULL DEFAULT false,
    author_id integer,
    editor_id integer,
    deleted_at timestamp without time zone,
    searchable tsvector,
    lang integer NOT NULL DEFAULT 1,
    related_id integer,
    CONSTRAINT gotorussia_travels_tours_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.gotorussia_travels_tours
    OWNER to "user";

GRANT ALL ON TABLE public.gotorussia_travels_tours TO "user";

-- Index: gotorussia_travels_tours_areaid_index

-- DROP INDEX public.gotorussia_travels_tours_areaid_index;

CREATE INDEX gotorussia_travels_tours_areaid_index
    ON public.gotorussia_travels_tours USING btree
    (area_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_cat_idx

-- DROP INDEX public.gotorussia_travels_tours_cat_idx;

CREATE INDEX gotorussia_travels_tours_cat_idx
    ON public.gotorussia_travels_tours USING btree
    (category_id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_id_idx

-- DROP INDEX public.gotorussia_travels_tours_id_idx;

CREATE UNIQUE INDEX gotorussia_travels_tours_id_idx
    ON public.gotorussia_travels_tours USING btree
    (id ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_latlon_idx

-- DROP INDEX public.gotorussia_travels_tours_latlon_idx;

CREATE INDEX gotorussia_travels_tours_latlon_idx
    ON public.gotorussia_travels_tours USING btree
    (lat ASC NULLS LAST, lon ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_localid_sort_index

-- DROP INDEX public.gotorussia_travels_tours_localid_sort_index;

CREATE UNIQUE INDEX gotorussia_travels_tours_localid_sort_index
    ON public.gotorussia_travels_tours USING btree
    (local_id ASC NULLS LAST, lang ASC NULLS LAST, sort_order DESC NULLS FIRST, id ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE moderated IS TRUE AND deleted_at IS NULL;
-- Index: gotorussia_travels_tours_localprice_idx

-- DROP INDEX public.gotorussia_travels_tours_localprice_idx;

CREATE INDEX gotorussia_travels_tours_localprice_idx
    ON public.gotorussia_travels_tours USING btree
    (local_id ASC NULLS LAST, ((tour_json ->> 'price_from'::text)::double precision) ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_lonlat_idx

-- DROP INDEX public.gotorussia_travels_tours_lonlat_idx;

CREATE INDEX gotorussia_travels_tours_lonlat_idx
    ON public.gotorussia_travels_tours USING btree
    (lon ASC NULLS LAST, lat ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_moderated_idx

-- DROP INDEX public.gotorussia_travels_tours_moderated_idx;

CREATE INDEX gotorussia_travels_tours_moderated_idx
    ON public.gotorussia_travels_tours USING btree
    (moderated ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_recommend_idx

-- DROP INDEX public.gotorussia_travels_tours_recommend_idx;

CREATE INDEX gotorussia_travels_tours_recommend_idx
    ON public.gotorussia_travels_tours USING btree
    (recommend ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_regionid_index

-- DROP INDEX public.gotorussia_travels_tours_regionid_index;

CREATE INDEX gotorussia_travels_tours_regionid_index
    ON public.gotorussia_travels_tours USING btree
    (region_id ASC NULLS LAST)
    TABLESPACE pg_default
    WHERE moderated IS TRUE;
-- Index: gotorussia_travels_tours_slots_idx

-- DROP INDEX public.gotorussia_travels_tours_slots_idx;

CREATE INDEX gotorussia_travels_tours_slots_idx
    ON public.gotorussia_travels_tours USING btree
    (((tour_json ->> 'slots'::text)::integer) ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_slug_index

-- DROP INDEX public.gotorussia_travels_tours_slug_index;

CREATE UNIQUE INDEX gotorussia_travels_tours_slug_index
    ON public.gotorussia_travels_tours USING btree
    (slug COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_sort_idx

-- DROP INDEX public.gotorussia_travels_tours_sort_idx;

CREATE INDEX gotorussia_travels_tours_sort_idx
    ON public.gotorussia_travels_tours USING btree
    (sort_order DESC NULLS FIRST)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_trgrm_title_idx

-- DROP INDEX public.gotorussia_travels_tours_trgrm_title_idx;

CREATE INDEX gotorussia_travels_tours_trgrm_title_idx
    ON public.gotorussia_travels_tours USING btree
    (tour_title)
    TABLESPACE pg_default;
-- Index: gotorussia_travels_tours_trgrm_title_moderated_idx

-- DROP INDEX public.gotorussia_travels_tours_trgrm_title_moderated_idx;

CREATE INDEX gotorussia_travels_tours_trgrm_title_moderated_idx
    ON public.gotorussia_travels_tours USING btree
    (tour_title)
    TABLESPACE pg_default
    WHERE moderated IS TRUE;
-- Index: tours_searchable_index

-- DROP INDEX public.tours_searchable_index;

CREATE INDEX tours_searchable_index
    ON public.gotorussia_travels_tours USING gin
    (searchable)
    TABLESPACE pg_default;

    """
    )
