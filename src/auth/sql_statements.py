get_user_by_id_stmt: str = """
    SELECT *
    FROM users
    WHERE users.id = :user_id
"""

get_all_users_stmt: str = """
    SELECT *
    FROM users
    ORDER BY users.id DESC
"""
