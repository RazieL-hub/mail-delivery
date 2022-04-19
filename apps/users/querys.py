add_user_query = """
insert into users(email, telegram, viber, whats_app, user_id) 
values (:email, :telegram, :viber, :whats_app, :user_id)
"""
update_user_query = """
update users set email = :email, telegram = :telegram, viber = :viber, whats_app = :whats_app
where user_id = :user_id
"""
delete_user_query = """
delete from users where user_id = :user_id
"""
get_user_query = """
select * from users where user_id =:user_id
"""
