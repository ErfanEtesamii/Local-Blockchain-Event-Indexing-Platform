from fastapi import APIRouter, Query

from app.api.database import get_connection

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.get("")
def list_transfers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    from_address: str | None = Query(default=None),
):
    offset = (page - 1) * limit

    where_clause = ""
    params = []

    if from_address:
        where_clause = "WHERE from_address = %s"
        params.append(from_address)

    with get_connection() as conn:
        with conn.cursor() as cur:

            count_query = f"""
                SELECT COUNT(*) AS total
                FROM token_transfers
                {where_clause}
            """

            cur.execute(count_query, params)
            total = cur.fetchone()["total"]

            data_query = f"""
                SELECT
                    id,
                    tx_hash,
                    block_number,
                    event_index,
                    from_address,
                    to_address,
                    token_address,
                    amount::text AS amount,
                    status,
                    processed_at,
                    created_at
                FROM token_transfers
                {where_clause}
                ORDER BY id DESC
                LIMIT %s OFFSET %s
            """

            cur.execute(
                data_query,
                params + [limit, offset],
            )

            rows = cur.fetchall()

    return {
        "data": rows,
        "meta": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit if total else 0,
        },
    }