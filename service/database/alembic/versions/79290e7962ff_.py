"""

Revision ID: 79290e7962ff
Revises: 9e306dabae18
Create Date: 2021-03-27 14:12:48.814147

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '79290e7962ff'
down_revision = '9e306dabae18'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'news',
        sa.Column('news_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('news_id'),
    )
    op.create_index(op.f('ix_news_news_id'), 'news', ['news_id'], unique=False)
    op.create_table(
        'trips',
        sa.Column('trip_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('trip_id'),
    )
    op.create_index(op.f('ix_trips_trip_id'), 'trips', ['trip_id'], unique=False)

    conn = op.get_bind()
    conn.execute(
        """
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
        """
    )


def downgrade():
    op.drop_index(op.f('ix_trips_trip_id'), table_name='trips')
    op.drop_table('trips')
    op.drop_index(op.f('ix_news_news_id'), table_name='news')
    op.drop_table('news')

    raise RuntimeError('Not downgradable')
    # ### end Alembic commands ###
