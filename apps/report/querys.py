create_task = """INSERT INTO reports(user_id, type_event, report_data, status, date_created) 
VALUES (:user_id, :type_event, :report_data, :status, :date_created)"""

update_task_status = """UPDATE reports set status = true where id = :task_id"""

get_task_query = """select * from reports where user_id=:user_id 
and type_event=:type_event 
and status=:status
"""