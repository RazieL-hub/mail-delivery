create_task = """INSERT INTO reports(status) VALUES (:status) RETURNING id"""
update_task_status = """UPDATE reports set status = true where id = :task_id"""