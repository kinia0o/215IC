"# 215IC" 
#### 1. Selecting Constant
```bash 
select 1;
```
![query1](screeny/query1.png)

#### 2.Selecting All Values from Table
```bash 
select * from little_penguins;
```
![query2](screeny/query2.png)

#### 3. Specifying Columns
```bash 
select
    species,
    island,
    sex
from little_penguins;
```
![query3](screeny/query3.png)

#### 4. Sorting
```bash 
select
    species,
    sex,
    island
from little_penguins
order by island asc, sex desc;
```
![query4](screeny/query4.png)

#### Exercise 1
```bash 
SELECT sex, body_mass_g
FROM little_penguins
ORDER BY body_mass_g DESC;
```
![exercise1](screeny/exercise1.png)

#### 5. Limiting Output
```bash 
select
    species,
    sex,
    island
from penguins
order by species, sex, island
limit 10;
```
![query5](screeny/query5.png)

#### 6. Paging Output
```bash 
select
    species,
    sex,
    island
from penguins
order by species, sex, island
limit 10 offset 3;
```
![query6](screeny/query6.png)

#### 7. Removing Duplicates
```bash 
select distinct
    species,
    sex,
    island
from penguins;
```
![query7](screeny/query7.png)

#### Exercise 2
Write a SQL query to select the islands and species from rows 50 to 60 inclusive of the penguins table. Your result should have 11 rows.
```bash 
SELECT island, species
FROM little_penguins
LIMIT 10 OFFSET 49;
```
Modify your query to select distinct combinations of island and species from the same rows and compare the result to what you got in part 1.
```bash 
SELECT DISTINCT island, species
FROM little_penguins
LIMIT 10 OFFSET 49;
```
#### 8. Filtering Results
```bash 
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe';
```
![query8](screeny/query8.png)

#### Exercise 3

Write a query to select the body masses from penguins that are less than 3000.0 grams.
```bash 
SELECT body_mass_g
FROM penguins
WHERE body_mass_g < 3000.0;
```
![exercise3p1](screeny/exercise3p1.png)

Write another query to select the species and sex of penguins that weight less than 3000.0 grams. This shows that the columns displayed and those used in filtering are independent of each other.
```bash 
SELECT species, sex
FROM penguins
WHERE body_mass_g < 3000.0;
```
![exercise3p2](screeny/exercise3p2.png)

#### 9. Filtering with More Complex Conditions
```bash 
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe' and sex != 'MALE';
```
![query9](screeny/query9.png)

#### Exercise 4

Use the not operator to select penguins that are not Gentoos.
```bash 
SELECT 
    species,
    sex,
    island
FROM penguins
WHERE species != 'Gentoo';
```
![exercise4p1](screeny/exercise4p1.png)

SQL’s or is an inclusive or: it succeeds if either or both conditions are true. SQL does not provide a specific operator for exclusive or, which is true if either but not both conditions are true, but the same effect can be achieved using and, or, and not. Write a query to select penguins that are female or on Torgersen Island but not both.
```bash 
SELECT 
    species,
    sex,
    island
FROM penguins
WHERE (sex = 'female' OR island = 'Torgersen') AND NOT (sex = 'female' AND island = 'Torgersen');
```
![exercise4p2](screeny/exercise4p2.png)

#### 10. Doing Calculations
```bash 
select
    flipper_length_mm / 10.0,
    body_mass_g / 1000.0
from penguins
limit 3;
```
![query10](screeny/query10.png)

#### 11. Renaming Columns
```bash 
select
    flipper_length_mm / 10.0 as flipper_cm,
    body_mass_g / 1000.0 as weight_kg,
    island as where_found
from penguins
limit 3;
```
![query11](screeny/query11.png)

#### Exercise 5

Write a single query that calculates and returns:

A column called what_where that has the species and island of each penguin separated by a single space.
A column called bill_ratio that has the ratio of bill length to bill depth.
You can use the || operator to concatenate text to solve part 1, or look at the documentation for SQLite’s format() function.
```bash 
SELECT species || ' ' || island AS what_where,
       bill_length_mm / bill_depth_mm AS bill_ratio
FROM penguins;
```
![exercise5](screeny/exercise5.png)

#### 12. Calculating with Missing Values
```bash 
select
    flipper_length_mm / 10.0 as flipper_cm,
    body_mass_g / 1000.0 as weight_kg,
    island as where_found
from penguins
limit 5;
```
![query12](screeny/query12.png)

#### 13. Null Equality
Part1
```bash 
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe';
```
![query13p1](screeny/query13p1.png)

#### Part 2
```bash 
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe' and sex = 'FEMALE';
```
![query13p2](screeny/query13p2.png)

#### 14. Null Inequality
```bash 
select distinct
    species,
    sex,
    island
from penguins
where island = 'Biscoe' and sex != 'FEMALE';
```
![query14](screeny/query14.png)

#### 15. Ternary Logic
```bash 
select null = null;

![query15](screeny/query15.png)
```
#### 16. Handling Null Safely
```bash 
select
    species,
    sex,
    island
from penguins
where sex is null;
```
![query16](screeny/query16.png)

#### Exercise 6

Write a query to find penguins whose body mass is known but whose sex is not.
```bash 
SELECT *
FROM penguins
WHERE body_mass_g IS NOT NULL
  AND sex IS NULL;
```
![exercise6p2](screeny/exercise6p1.png)

Write another query to find penguins whose sex is known but whose body mass is not.
```bash 
SELECT *
FROM penguins
WHERE body_mass_g IS NULL
  AND sex IS NOT NULL;
```
![exercise6p2](screeny/exercise6p2.png)

 ####  17. Aggregating
```bash 
  select sum(body_mass_g) as total_mass
from penguins;
```
![query17](screeny/query17.png)

#### 18. Common Aggregation Functions
```bash 
select
    max(bill_length_mm) as longest_bill,
    min(flipper_length_mm) as shortest_flipper,
    avg(bill_length_mm) / avg(bill_depth_mm) as weird_ratio
from penguins;
```
![query18](screeny/query18.png)

#### Exercise 7

What is the average body mass of penguins that weight more than 3000.0 grams?
```bash 
SELECT AVG(body_mass_g) AS average_body_mass
FROM penguins
WHERE body_mass_g > 3000.0;
```
![exercise7](screeny/exercise7.png)

#### 19. Counting
```bash 
select
    count(*) as count_star,
    count(sex) as count_specific,
    count(distinct sex) as count_distinct
from penguins;
```
![query19](screeny/query19.png)

#### Exercise 8
How many different body masses are in the penguins dataset?
```bash 
SELECT COUNT(DISTINCT body_mass_g) AS distinct_body_masses
FROM penguins;
```
![exercise8](screeny/exercise8.png)

#### 20. Grouping
```bash 
select avg(body_mass_g) as average_mass_g
from penguins
group by sex;
```
![query20](screeny/query20.png)

#### 21. Behavior of Unaggregated Columns
```bash 
select
    sex,
    avg(body_mass_g) as average_mass_g
from penguins
group by sex;
```
![query21](screeny/query21.png)

#### 22. Arbitrary Choice in Aggregation
```bash 
select
    sex,
    body_mass_g
from penguins
group by sex;
```
![query22](screeny/query22.png)

#### Exercise 9

Explain why the output of the previous query has a blank line before the rows for female and male penguins.

Write a query that shows each distinct body mass in the penguin dataset and the number of penguins that weigh that much.
```bash 
SELECT body_mass_g, COUNT(*) AS num_penguins
FROM penguins
GROUP BY body_mass_g
ORDER BY body_mass_g;
```
![exercise9](screeny/exercise9.png)

#### 23. Filtering Aggregated Values
```bash 
select
    sex,
    avg(body_mass_g) as average_mass_g
from penguins
group by sex
having average_mass_g > 4000.0;
```
![query23](screeny/query23.png)

#### 24. Readable Output
```bash 
select
    sex,
    round(avg(body_mass_g), 1) as average_mass_g
from penguins
group by sex
having average_mass_g > 4000.0;
```
![query24](screeny/query24.png)

#### 25. Filtering Aggregate Inputs
```bash 
select
    sex,
    round(
        avg(body_mass_g) filter (where body_mass_g < 4000.0),
        1
    ) as average_mass_g
from penguins
group by sex;
```
![query25](screeny/query25.png)

#### Exercise 10

Write a query that uses filter to calculate the average body masses of heavy penguins (those over 4500 grams) and light penguins (those under 3500 grams) simultaneously. Is it possible to do this using where instead of filter?
```bash 
SELECT
    AVG(CASE WHEN body_mass_g > 4500 THEN body_mass_g END) AS average_body_mass_heavy,
    AVG(CASE WHEN body_mass_g < 3500 THEN body_mass_g END) AS average_body_mass_light
FROM penguins;

![exercise10](screeny/exercise10.png)
```
#### 26. Creating In-memory Database
```bash 
sqlite3 :memory:
```
#### 27. Creating Tables
```bash 
create table job (
    name text not null,
    billable real not null
);
create table work (
    person text not null,
    job text not null
);
```
![query27](screeny/query27.png)

#### 28. Inserting Data
```bash 
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
```
![query28](screeny/query28.png)

#### Exercise 11

Using an in-memory database, define a table called notes with two text columns author and note and then add three or four rows. Use a query to check that the notes have been stored and that you can (for example) select by author name.

What happens if you try to insert too many or too few values into notes? What happens if you insert a number instead of a string into the note field?
```bash 
CREATE TABLE notes (
    author TEXT,
    note TEXT
);
```
![exercise11p1](screeny/exercise11p1.png)
```bash 
INSERT INTO notes (author, note) VALUES
    ('Alicja', 'first note'),
    ('Arek', 'second note'),
    ('Bartek', 'third note');
```
![exercise11p2](screeny/exercise11p2.png)
```bash 
INSERT INTO notes (author, note) VALUES
    ('Antek', '4th note', 'cos');
```
![exercise11p3](screeny/exercise11p3.png)
```bash 
INSERT INTO notes (author) VALUES
    ('Robert');
```
![exercise11p4](screeny/exercise11p4.png)
```bash 
SELECT * FROM notes;
```
#### 29. Updating Rows

```bash 
update work
set person = 'tae'
where person = 'tay';
```
![query29](screeny/query29.png)

#### 30. Deleting Rows
```bash 
delete from work
where person = 'tae';

select * from work;
```
![query30](screeny/query30.png)

#### Exercise 12

What happens if you try to delete rows that don’t exist (e.g., all entries in work that refer to juna)?

Query will execute correctly, even if nothing is delete.

![exercise12](screeny/exercise12.png)

#### 31. Backing Up
```bash 
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
```
![query31](screeny/query31.png)

#### 32. Combining Information
```bash 
select *
from work cross join job;
```


#### 33. Inner Join
```bash 
select *
from work inner join job
    on work.job = job.name;
```
![query33](screeny/query33.png)

#### Exercise 13

Re-run the query shown above using where job = name instead of the full table.name notation. Is the shortened form easier or harder to read and more or less likely to cause errors?
```bash 
select *
from work inner join job
    on job = name;
```
![exercise13](screeny/exercise13.png)

34. Aggregating Joined Data
```bash 
select
    work.person,
    sum(job.billable) as pay
from work inner join job
    on work.job = job.name
group by work.person;
```
![query34](screeny/query34.png)

#### 35. Left Join
```bash 
select *
from work left join job
    on work.job = job.name;
```
![query35](screeny/query35.png)

#### 36. Aggregating Left Joins
```bash 
select
    work.person,
    sum(job.billable) as pay
from work left join job
    on work.job = job.name
group by work.person;
```
![query36](screeny/query36.png)

#### 37. Coalescing Values
```bash 
select
    work.person,
    coalesce(sum(job.billable), 0.0) as pay
from work left join job
    on work.job = job.name
group by work.person;
```
![query37](screeny/query37.png)

#### 38. Full Outer Join
```bash 
create table size (
    s text not null
);
insert into size values ('light'), ('heavy');

create table weight (
    w text not null
);

select * from size full outer join weight;

```
#### 39. Negating Incorrectly
```bash 
select distinct person
from work
where job != 'calibrate';
```
![query39](screeny/query39.png)

#### 40. Set Membership
```bash 
select *
from work
where person not in ('mik', 'tay');
```
![query40](screeny/query40.png)

#### 41. Subqueries
```bash 
select distinct person
from work
where person not in (
    select distinct person
    from work
    where job = 'calibrate'
);
```
![query41](screeny/query41.png)

#### 42. Defining a Primary Key
```bash 
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
```
![query42p1](screeny/query42p1.png)
```bash 
insert into lab_equipment values
(1.5, 'green', 2);
```
![query42p2](screeny/query42p2.png)

#### Exercise
Does the penguins table have a primary key? If so, what is it? What about the work and job tables?

#### 43. Autoincrementing and Primary Keys
```bash 
create table person (
    ident integer primary key autoincrement,
    name text not null
);
```
![query43p1](screeny/query43p1.png)
```bash 
insert into person values
(null, 'mik'),
(null, 'po'),
(null, 'tay');
select * from person;
insert into person values (1, 'prevented');
```
![query43p2](screeny/query43p2.png)

#### 44. Internal Tables
```bash 
select * from sqlite_sequence;
```
![query44](screeny/query44.png)

#### Exercise
Are you able to modify the values stored in sqlite_sequence? In particular, are you able to reset the values so that the same sequence numbers are generated again?

We are not able to modify directly, we only can:
- Dropping and recreating the table with the AUTOINCREMENT column.
- Inserting data into the table again, starting the sequence numbers from 1.

#### 45. Altering Tables
```bash 
alter table job
add ident integer not null default -1;

update job
set ident = 1
where name = 'calibrate';

update job
set ident = 2
where name = 'clean';

select * from job;
```
![query45](screeny/query45.png)



