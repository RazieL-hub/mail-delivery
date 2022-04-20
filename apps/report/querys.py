create_task = """INSERT INTO reports(user_id, type_event_id, report_data, status, date_created) 
VALUES (:user_id, :type_event_id, :report_data, :status, :date_created)"""

update_task_status = """UPDATE reports set status = true where id = :task_id"""

get_task_query = """select from reports where user_id=:user_id 
and type_event_id=:type_event_id 
and status=:status
"""
get_task_for_user = """
select * from reports where status=FALSE GROUP BY user_id and type_event_id
"""
