from app import create_app



app = create_app()

@app.shell_context_processor
def make_shell_context():
    from db import get_db, query_db, change_db
    conn = get_db()
    return dict(conn=conn, cur=conn.cursor(), query_db=query_db, change_db=change_db)