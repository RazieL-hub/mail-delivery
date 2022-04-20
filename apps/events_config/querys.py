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

get_test_event_all = """
select * from reports where status=:status
"""

update_all_task = """
update reports set status = :new_status 
where status=:old_status
"""