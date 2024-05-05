"# 215IC" 
1. Selecting Constant

select 1;

2.Selecting All Values from Table

select * from little_penguins;

3. Specifying Columns

select
    species,
    island,
    sex
from little_penguins;

4. Sorting

select
    species,
    sex,
    island
from little_penguins
order by island asc, sex desc;

Exercise 1

SELECT sex, body_mass_g
FROM little_penguins
ORDER BY body_mass_g DESC;

5. Limiting Output

select
    species,
    sex,
    island
from penguins
order by species, sex, island
limit 10;

6. Paging Output

select
    species,
    sex,
    island
from penguins
order by species, sex, island
limit 10 offset 3;

7. Removing Duplicates

select distinct
    species,
    sex,
    island
from penguins;

Exercise 2
Write a SQL query to select the islands and species from rows 50 to 60 inclusive of the penguins table. Your result should have 11 rows.

SELECT island, species
FROM little_penguins
LIMIT 10 OFFSET 49;

Modify your query to select distinct combinations of island and species from the same rows and compare the result to what you got in part 1.

SELECT DISTINCT island, species
FROM little_penguins
LIMIT 10 OFFSET 49;

8. Filtering Results

select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe';

Exercise 3

Write a query to select the body masses from penguins that are less than 3000.0 grams.

SELECT body_mass_g
FROM penguins
WHERE body_mass_g < 3000.0;

Write another query to select the species and sex of penguins that weight less than 3000.0 grams. This shows that the columns displayed and those used in filtering are independent of each other.

SELECT species, sex
FROM penguins
WHERE body_mass_g < 3000.0;

9. Filtering with More Complex Conditions

select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe' and sex != 'MALE';

Exercise 4

Use the not operator to select penguins that are not Gentoos.

SELECT 
    species,
    sex,
    island
FROM penguins
WHERE species != 'Gentoo';

SQL’s or is an inclusive or: it succeeds if either or both conditions are true. SQL does not provide a specific operator for exclusive or, which is true if either but not both conditions are true, but the same effect can be achieved using and, or, and not. Write a query to select penguins that are female or on Torgersen Island but not both.

SELECT 
    species,
    sex,
    island
FROM penguins
WHERE (sex = 'female' OR island = 'Torgersen') AND NOT (sex = 'female' AND island = 'Torgersen');

10. Doing Calculations

select
    flipper_length_mm / 10.0,
    body_mass_g / 1000.0
from penguins
limit 3;

11. Renaming Columns

select
    flipper_length_mm / 10.0 as flipper_cm,
    body_mass_g / 1000.0 as weight_kg,
    island as where_found
from penguins
limit 3;

Exercise 5

Write a single query that calculates and returns:

A column called what_where that has the species and island of each penguin separated by a single space.
A column called bill_ratio that has the ratio of bill length to bill depth.
You can use the || operator to concatenate text to solve part 1, or look at the documentation for SQLite’s format() function.

SELECT species || ' ' || island AS what_where,
       bill_length_mm / bill_depth_mm AS bill_ratio
FROM penguins;

12. Calculating with Missing Values

select
    flipper_length_mm / 10.0 as flipper_cm,
    body_mass_g / 1000.0 as weight_kg,
    island as where_found
from penguins
limit 5;

13. Null Equality
Part1
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe';

Part 2
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe' and sex = 'FEMALE';

14. Null Inequality

select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe' and sex != 'FEMALE';

15. Ternary Logic

select null = null;

16. Handling Null Safely

select
    species,
    sex,
    island
from penguins
where sex is null;

Exercise 6

Write a query to find penguins whose body mass is known but whose sex is not.

SELECT *
FROM penguins
WHERE body_mass_g IS NOT NULL
  AND sex IS NULL;

Write another query to find penguins whose sex is known but whose body mass is not.

SELECT *
FROM penguins
WHERE body_mass_g IS NULL
  AND sex IS NOT NULL;

  17. Aggregating

  select sum(body_mass_g) as total_mass
from penguins;

18. Common Aggregation Functions

select
    max(bill_length_mm) as longest_bill,
    min(flipper_length_mm) as shortest_flipper,
    avg(bill_length_mm) / avg(bill_depth_mm) as weird_ratio
from penguins;

Exercise 7

What is the average body mass of penguins that weight more than 3000.0 grams?

SELECT AVG(body_mass_g) AS average_body_mass
FROM penguins
WHERE body_mass_g > 3000.0;

19. Counting

select
    count(*) as count_star,
    count(sex) as count_specific,
    count(distinct sex) as count_distinct
from penguins;

Exercise 8
How many different body masses are in the penguins dataset?

SELECT COUNT(DISTINCT body_mass_g) AS distinct_body_masses
FROM penguins;

20. Grouping

select avg(body_mass_g) as average_mass_g
from penguins
group by sex;

21. Behavior of Unaggregated Columns

select
    sex,
    avg(body_mass_g) as average_mass_g
from penguins
group by sex;

22. Arbitrary Choice in Aggregation

select
    sex,
    body_mass_g
from penguins
group by sex;

Exercise 9

Explain why the output of the previous query has a blank line before the rows for female and male penguins.

Write a query that shows each distinct body mass in the penguin dataset and the number of penguins that weigh that much.

SELECT body_mass_g, COUNT(*) AS num_penguins
FROM penguins
GROUP BY body_mass_g
ORDER BY body_mass_g;

23. Filtering Aggregated Values

select
    sex,
    avg(body_mass_g) as average_mass_g
from penguins
group by sex
having average_mass_g > 4000.0;

24. Readable Output

select
    sex,
    round(avg(body_mass_g), 1) as average_mass_g
from penguins
group by sex
having average_mass_g > 4000.0;

25. Filtering Aggregate Inputs

select
    sex,
    round(
        avg(body_mass_g) filter (where body_mass_g < 4000.0),
        1
    ) as average_mass_g
from penguins
group by sex;

Exercise 10

Write a query that uses filter to calculate the average body masses of heavy penguins (those over 4500 grams) and light penguins (those under 3500 grams) simultaneously. Is it possible to do this using where instead of filter?

SELECT
    AVG(CASE WHEN body_mass_g > 4500 THEN body_mass_g END) AS average_body_mass_heavy,
    AVG(CASE WHEN body_mass_g < 3500 THEN body_mass_g END) AS average_body_mass_light
FROM penguins;

26. Creating In-memory Database
sqlite3 :memory:

27. Creating Tables

create table job (
    name text not null,
    billable real not null
);
create table work (
    person text not null,
    job text not null
);

28. Inserting Data

insert into job values
('calibrate', 1.5),
('clean', 0.5);
insert into work values
('mik', 'calibrate'),
('mik', 'clean'),
('mik', 'complain'),
('po', 'clean'),
('po', 'complain'),
('tay', 'complain');

Exercise 11

Using an in-memory database, define a table called notes with two text columns author and note and then add three or four rows. Use a query to check that the notes have been stored and that you can (for example) select by author name.

What happens if you try to insert too many or too few values into notes? What happens if you insert a number instead of a string into the note field?

CREATE TABLE notes (
    author TEXT,
    note TEXT
);

INSERT INTO notes (author, note) VALUES
    ('Alicja', 'first note'),
    ('Arek', 'second note'),
    ('Bartek', 'third note');

INSERT INTO notes (author, note) VALUES
    ('Antek', '4th note', 'cos');

INSERT INTO notes (author) VALUES
    ('Robert');

SELECT * FROM notes;

29. Updating Rows


update work
set person = 'tae'
where person = 'tay';

30. Deleting Rows

delete from work
where person = 'tae';

select * from work;

Exercise 12

What happens if you try to delete rows that don’t exist (e.g., all entries in work that refer to juna)?

Query will execute correctly, even if nothing is delete.

31. Backing Up

create table backup (
    person text not null,
    job text not null
);

insert into backup
select
    person,
    job
from work
where person = 'tae';

delete from work
where person = 'tae';

select * from backup;

32. Combining Information
select *
from work cross join job;

33. Inner Join

select *
from work inner join job
    on work.job = job.name;

Exercise 13

Re-run the query shown above using where job = name instead of the full table.name notation. Is the shortened form easier or harder to read and more or less likely to cause errors?

select *
from work inner join job
    on job = name;

34. Aggregating Joined Data

select
    work.person,
    sum(job.billable) as pay
from work inner join job
    on work.job = job.name
group by work.person;

35. Left Join

select *
from work left join job
    on work.job = job.name;

36. Aggregating Left Joins

select
    work.person,
    sum(job.billable) as pay
from work left join job
    on work.job = job.name
group by work.person;

37. Coalescing Values

select
    work.person,
    coalesce(sum(job.billable), 0.0) as pay
from work left join job
    on work.job = job.name
group by work.person;

38. Full Outer Join

create table size (
    s text not null
);
insert into size values ('light'), ('heavy');

create table weight (
    w text not null
);

select * from size full outer join weight;

39. Negating Incorrectly

select distinct person
from work
where job != 'calibrate';

40. Set Membership

select *
from work
where person not in ('mik', 'tay');

41. Subqueries

select distinct person
from work
where person not in (
    select distinct person
    from work
    where job = 'calibrate'
);

42. Defining a Primary Key

create table lab_equipment (
    size real not null,
    color text not null,
    num integer not null,
    primary key (size, color)
);

insert into lab_equipment values
(1.5, 'blue', 2),
(1.5, 'green', 1),
(2.5, 'blue', 1);

select * from lab_equipment;

insert into lab_equipment values
(1.5, 'green', 2);

Exercise
Does the penguins table have a primary key? If so, what is it? What about the work and job tables?

43. Autoincrementing and Primary Keys

create table person (
    ident integer primary key autoincrement,
    name text not null
);
insert into person values
(null, 'mik'),
(null, 'po'),
(null, 'tay');
select * from person;
insert into person values (1, 'prevented');

44. Internal Tables

select * from sqlite_sequence;

Exercise
Are you able to modify the values stored in sqlite_sequence? In particular, are you able to reset the values so that the same sequence numbers are generated again?

We are not able to modify directly, we only can:
- Dropping and recreating the table with the AUTOINCREMENT column.
- Inserting data into the table again, starting the sequence numbers from 1.

45. Altering Tables

alter table job
add ident integer not null default -1;

update job
set ident = 1
where name = 'calibrate';

update job
set ident = 2
where name = 'clean';

select * from job;