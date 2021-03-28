from typing import Any

from sqlalchemy import cast, func, or_
from sqlalchemy.orm import Query, Session

from database import Category, Location, Region


def get_pop_region_categories(db: Session, name: str) -> Any:
    region_id = db.execute(
        'SELECT orig_id from gotorussia_travels_regions where name = :name', {'name': name}
    ).fetchone()['orig_id']
    result = db.execute(
        """SELECT category_id, name FROM (
     SELECT b        AS category_id,
            count(*) AS count
     FROM (SELECT id,
                  TRIM(BOTH '\"'
                       FROM CAST(JSONB_ARRAY_ELEMENTS(type_id) AS varchar)) AS b
           FROM gotorussia_travels_locations
           WHERE local_id = :region_id) AS foo
     GROUP BY category_id
 ) as bar
 LEFT JOIN gotorussia_types_category ON bar.category_id = CAST(gotorussia_types_category.id as varchar)
ORDER BY count DESC
LIMIT 10;""",
        {'region_id': region_id},
    ).fetchall()
    return result


def get_locations_by_region_name(db: Session, name: str) -> Any:
    region_id = db.execute(
        'SELECT orig_id from gotorussia_travels_regions where name = :name', {'name': name}
    ).fetchone()['orig_id']
    result = db.execute("SELECT * from gotorussia_travels_locations where local_id = :region_id",
                        {'region_id': region_id}
                        ).fetchall()
    return result[:10]
