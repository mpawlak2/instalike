create table users(id bigint primary key,
		    username varchar(500),
		    has_blocked_viewer boolean,
		    follows_count integer,
		    followed_by_count integer,
		    external_url varchar,
		    follows_viewer boolean,
		    profile_pic_url varchar(1000),
		    is_private boolean,
		    full_name varchar(500),   
		    posts_count integer,
		    blocked_by_viewer boolean,
		    followed_by_viewer boolean,
		    is_verified boolean,
		    biography varchar(1000));

create table photos 
	(id int primary key,
	code varchar(100) unique,
	width int,
	height int,
	is_ad boolean,
	likes_count int,
	is_video boolean,
	display_src varchar(500),
	loc varchar(500));--,
	--owner_fk integer REFERENCES users(id));

create table opcodes (
		id integer primary key,
		op_name varchar(100)
	);

insert into opcodes (id, op_name) values (1, 'like'), (2, 'unlike'), (3, 'follow'), (4, 'unfollow'), (5, 'block user'), (6, 'comment');
	
create table likes(id serial primary key, photo_id bigint REFERENCES photos (id), status_code int, like_time timestamp);

create or replace function merge_photo(
	_id bigint,
	_width integer,
	_height integer,
	_code varchar,
	_is_ad boolean,
	_likes_count integer,
	_viewer_has_liked boolean,
	_is_video boolean,
	_display_src varchar,
	_location varchar)
returns boolean as $$
begin
	if _id is null then
		return false;
	end if;

	if photo_exists(_id) then
		update photos
		set
			likes_count = _likes_count,
			display_src = _display_src
		where id = _id;
	else
		insert into photos (id, code, width, height, is_ad, likes_count, is_video, display_src, loc)
		values (_id, _code, _width, _height, _is_ad, _likes_count, _is_video, _display_src, _location);
	end if;
	
	return true;
end;
$$ language plpgsql;

create or replace function photo_exists(photo_id bigint)
returns boolean
as $$
begin
	return exists(select null from photos where id = photo_id);
end
$$ language plpgsql;


create or replace function merge_activity(id bigint)
returns boolean
as $$
-- store activities from your account
begin

end
$$ language plpgsql;


create or replace function like_photo(_photo_id bigint, _success boolean, _status_code integer)
returns boolean
as $$
begin
if exists(select null from likes where photo_id = _photo_id) then
return false;
end if;

insert into likes (photo_id, success, status_code, like_time) values (_photo_id, _success, _status_code, clock_timestamp());
return true;

end
$$ language plpgsql;



create table followers (id serial primary key, user_id bigint REFERENCES users (id), is_following boolean);

CREATE OR REPLACE FUNCTION public.merge_user(
    _id bigint,
    _username varchar,
    _has_blocked_viewer boolean,
    _follows_count integer,
    _followed_by_count integer,
    _external_url varchar,
    _follows_viewer boolean,
    _profile_pic_url varchar,
    _is_private boolean,
    _full_name varchar,   
    _posts_count integer,
    _blocked_by_viewer boolean,
    _followed_by_viewer boolean,
    _is_verified boolean,
    _biography varchar)
  RETURNS boolean AS
$$
begin
	if exists(select null from users where id = _id) then
		update users
		set
			follows_count = _follows_count,
			followed_by_count = _followed_by_count,
			follows_viewer = _follows_viewer,
			has_blocked_viewer = _has_blocked_viewer,
			blocked_by_viewer = _blocked_by_viewer,
			followed_by_viewer = _followed_by_viewer
		where id = _id;
		return true;
	end if;

	insert into users (id, username, has_blocked_viewer, follows_count, followed_by_count, external_url, follows_viewer, profile_pic_url, is_private,
		    full_name, posts_count, blocked_by_viewer, followed_by_viewer, is_verified, biography)
		values (_id, _username, _has_blocked_viewer, _follows_count, _followed_by_count, _external_url, _follows_viewer, _profile_pic_url, _is_private,
		    _full_name, _posts_count, _blocked_by_viewer, _followed_by_viewer, _is_verified, biography);

	return true;
end
$$ LANGUAGE plpgsql;

create table following (id serial primary key, user_id bigint REFERENCES users (id), status_code integer, start_following timestamp, stop_following timestamp);
create or replace function public.follow_user(_user_id bigint, _status_code int) 
returns boolean as
$$
begin
	insert into public.following(user_id, status_code, start_following) values (_user_id, _status_code, clock_timestamp());
	return true;
end
$$ language plpgsql;


-- activity
create table public.activities(id serial primary key, activity_type integer, user_id bigint, activity_time timestamp);
create or replace function public.register_activity(_type integer, _user_id bigint, _activity_time varchar)
returns boolean
as 
$$
declare 
	_activity_timestamp timestamp := to_timestamp(_activity_time);
begin 

	if exists(select null from activities where activity_time = _activity_timestamp and user_id = _user_id and activity_type = _type) then
		return false;
	end if;
	insert into public.activities(activity_type, user_id, activity_time) values(_type, _user_id, _activity_timestamp);
	return true;
end
$$ language plpgsql;

