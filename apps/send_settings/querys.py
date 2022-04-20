get_list_send_settings_query = """
select * from send_settings where user_id=:user_id
"""

get_send_settings_query = """
select * from send_settings where user_id=:user_id and type_event=:type_event
"""

add_settings_for_user_query = """
insert into send_settings(type_event, instant_delivery, periodic_time, work_time_start, work_time_finish, user_id, last_send)
values (:type_event, :instant_delivery, :periodic_time, :work_time_start, :work_time_finish, :user_id, :last_send)
"""

delete_settings_query = """
delete from send_settings where user_id=:user_id and type_event=:type_event
"""

update_settings_query = """
update send_settings set type_event = :type_event, instant_delivery = :instant_delivery, periodic_time = :periodic_time, 
work_time_start = :work_time_start, work_time_finish = :work_time_finish 
where user_id = :user_id and type_event=:type_event
"""