create_task = """INSERT INTO reports(user_id, type_event_id, report_data, status_send, date_created) 
VALUES (:user_id, :type_event_id, :report_data, :status_send, :date_created)"""

update_task_status = """UPDATE reports set status_send = true
where user_id = :user_id
and type_event_id = :type_event_id
and id in :reports_id"""

get_task_query = """select from reports where user_id=:user_id 
and type_event_id=:type_event_id 
and status=:status
"""

get_task_for_user = """
select * from reports where status_send=FALSE GROUP BY user_id and type_event_id
"""


count_messages_for_user_and_event = """
select user_id, type_event_id, count(*), MIN(date_created), MAX(date_created) from reports
where status_send=FALSE 
group by user_id, type_event_id
"""

get_one_report = """
select report_data from reports where prepare_message=True
and type_event_id = :type_event_id
and user_id = :user_id
and status_send 
"""

all_reports_status_false = """
select id from reports where status_send = FALSE 
"""

test = """
update reports set status_send=TRUE 
where id in :reports_id
"""


select_report = """
select id, report_data from reports 
where type_event_id = :type_event_id
and user_id = :user_id
and id in :reports_id
and status_send=FALSE
"""