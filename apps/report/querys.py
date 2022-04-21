create_task = """INSERT INTO reports(user_id, type_event_id, report_data, status_send, date_created, prepare_message) 
VALUES (:user_id, :type_event_id, :report_data, :status_send, :date_created, :prepare_message)"""

update_task_status = """UPDATE reports set status_send = true, prepare_message = false 
where user_id = :user_id
and type_event_id = :type_event_id
and status_send = false
and prepare_message = true"""

get_task_query = """select from reports where user_id=:user_id 
and type_event_id=:type_event_id 
and status=:status
"""
get_task_for_user = """
select * from reports where status_send=FALSE GROUP BY user_id and type_event_id
"""

task_prepare_to_send = """
UPDATE reports set prepare_message = true where status_send = false
"""

count_messages_for_user_and_event = """
select user_id, type_event_id, count(*), MIN(date_created), MAX(date_created) from reports
where prepare_message=True
group by user_id, type_event_id
"""

