get_list_send_settings_query = """
select * from events_config where user_id=:user_id
"""

get_event_config_query = """
select * from events_config where user_id=:user_id and type_event=:type_event
"""

add_settings_for_user_query = """
insert into events_config(type_event, instant_delivery, periodic_time, work_time_start, work_time_finish, user_id, last_send)
values (:type_event, :instant_delivery, :periodic_time, :work_time_start, :work_time_finish, :user_id, :last_send)
"""

delete_settings_query = """
delete from events_config where user_id=:user_id and type_event=:type_event
"""

update_settings_query = """
update events_config set type_event = :type_event, instant_delivery = :instant_delivery, periodic_time = :periodic_time, 
work_time_start = :work_time_start, work_time_finish = :work_time_finish 
where user_id = :user_id and type_event=:type_event
"""

get_events_ready_for_delivery = """
select report_data, date_creation from reports 
join events_config on reports.user_id = events_config.user_id, reports.type_event_id = events_config.id
join users on reports.user_id = users.user_id
where status_send=false
"""

update_all_task = """
update reports set status_send = :new_status 
where status_send=:old_status
"""

get_type_event_and_last_send = """
select type_event, last_send, periodic_time, work_time_start, work_time_finish, user_id
from events_config where id = :type_event_id
"""

update_last_send = """
update events_config set last_send=:date_time where id = :type_event_id
"""