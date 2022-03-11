queries = ["" for i in range(0, 25)]

queries[0] = """
select userid, name, birthdate, joined
from users
where extract(year from birthdate) = 1998 
order by birthdate ASC;
"""

queries[1] = """
SELECT *
FROM Users
WHERE name like 'Carol%'
ORDER by birthdate ASC;
"""

queries[2] = """
SELECT name, extract(year from age(joined, birthdate)) as age
FROM Users
ORDER by age ASC;
"""

queries[3] = """
SELECT distinct extract(year from birthdate) as year
FROM Users
WHERE name like 'M%'
ORDER by year ASC;
"""

queries[4] = """
SELECT name
FROM Users
WHERE extract(epoch from age(date '2021-08-31', joined)) / extract(epoch from age(date '2021-08-31', birthdate)) > 0.5
ORDER by name ASC;
"""

queries[5] = """
SELECT status_time, text
FROM Status 
JOIN (select * from Users where name = 'Kevin Allen') as K on Status.userid = K.userid
ORDER by status_time ASC;
"""

queries[6] = """
SELECT name, birthdate
FROM Users
WHERE (name like 'J%' and extract(year from birthdate) <= 1980) or (name like 'M%' and extract(year from birthdate) > 1980)
ORDER by name ASC;
"""


queries[7] = """
SELECT count(*) as num_friends
FROM Users u inner join friends on userid = userid1
WHERE name = 'Kevin Allen';
"""

queries[8] = """
SELECT count(*) as numusers
FROM Users
WHERE (name like 'A%') or (name like 'E%') or (name like 'I%') or (name like 'O%') or (name like 'U%');
"""


queries[9] = """
WITH temp as (select name, count(*) as num_friends from Users, Friends where users.userid = friends.userid1 group by name)
SELECT *
FROM temp
WHERE num_friends = (select max(num_friends) from temp);
"""

queries[10] = """
SELECT name
FROM Users
WHERE userid not in (select userid from Status)
ORDER by name ASC;
"""

queries[11] = """
SELECT
    n1.name as username,
    n2.name as friendname,
    n2.birthdate as friendbirthdate
FROM Users n1
    JOIN Friends as n3 on n1.userid  = n3.userid1
    JOIN Users as n2 on n3.userid2 = n2.userid
WHERE
    make_date(2021, extract(month from n2.birthdate)::int, extract(day from n2.birthdate)::int)
    between '2021-09-10' and '2021-09-25'
ORDER by username, friendname ASC;
"""

queries[12] = """
SELECT extract(year from birthdate) as birthyear, count(*) as num_users
FROM Users
GROUP by birthyear
ORDER by birthyear;
"""

queries[14] = """
WITH birthyears as (select * from generate_series(1940, 2000) as g(birthyear)), years as
(select extract(year from birthdate) as year, count(*) as num_users from users group by year)
SELECT birthyear, coalesce(num_users, 0) as num_users
FROM birthyears bd left join years yr on yr.year = bd.birthyear
ORDER by birthyear;
"""

queries[15] = """
WITH group_members as (select groupid, count(*) as num_members from members group by groupid)
SELECT name, num_members
FROM group_members groupmem join groups g on groupmem.groupid = g.groupid
WHERE num_members = (select max(num_members) from group_members)
ORDER by name ASC;
"""

queries[16] = """
WITH mike as (select userid as smith from users where name = 'Michael Smith') 
SELECT name, 'friends' as type from friends field join users on userid2 = userid, mike
WHERE field.userid1 = mike.smith
UNION
SELECT name, 'follows' as type
FROM follows field join users on userid2 = userid, mike
WHERE field.userid1 = mike.smith;
"""


queries[17] = """
WITH intersection as
(select * from friends intersect select * from follows)
SELECT usertable.userid, name, count(*) as num_common
FROM intersection inter join users usertable on inter.userid1 = usertable.userid
GROUP by usertable.userid, name
ORDER by name ASC;
"""


queries[18] = """
WITH pairs as (select lag(birthdate) over (order by birthdate asc) as bd1, lag(name) over
(order by birthdate asc) as u1, birthdate as bd2, name as u2 from users order by bd1 asc)
SELECT
    case when u1 < u2 then u1 else u2
    end as username1,
    case when u1 < u2 then u2 else u1
    end as username2
FROM pairs
WHERE bd2 - bd1 = (select min(bd2 - bd1) from pairs)
ORDER by u1;
"""

queries[19] = """
WITH friendcount as
(select userid1, count(*) as num_friends from friends group by userid1), followers_count as
(select userid2, count(*) as num_followers from follows group by userid2)
SELECT userid, name, coalesce(num_friends, 0) as num_friends, coalesce(num_followers, 0) as num_followers
FROM users usertable left join friendcount f1 on usertable.userid = f1.userid1 left join followers_count f2 on usertable.userid = f2.userid2 order by userid;
"""


queries[20] = """
SELECT name
FROM users usertable
WHERE not exists (select distinct userid2 from follows f1 where f1.userid1 in
(SELECT userid from members where groupid = 'group36') and f1.userid2 = usertable.userid)
ORDER by name ASC;
"""


queries[21] = """
drop table userscopy;
select * into userscopy from users;
alter table userscopy add column age integer, add column usage varchar(10);
"""

queries[22] = """
UPDATE userscopy
SET age = extract(year from age('2021-08-21', birthdate));
UPDATE userscopy ucopied
SET usage = (with counts as
(SELECT u.userid, coalesce(col.count, 0) as count from userscopy u left join
(SELECT userid, count(*) from status group by userid) col on u.userid = col.userid)
SELECT
    case
        when col.count < 5 then 'light'
        when col.count >= 5 and col.count <= 10 then 'medium'
        when col.count > 10 then 'heavy'
    end
FROM counts col
WHERE ucopied.userid = col.userid);
"""

queries[23] = """
DELETE from userscopy usertable
WHERE extract(month from usertable.birthdate) = 5;
"""

queries[24] = """
INSERT into userscopy (userid, name, birthdate, joined, age, usage)
SELECT 'newuser' || n, 'New User ' || n, date ('1990-01-' || n), date ('2015-01-' || n), 0, 'light'
FROM generate_series(11, 20) as s(n)
"""
