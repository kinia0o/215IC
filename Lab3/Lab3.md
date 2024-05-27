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


### 46. Comparing Individual Values to Aggregates
```bash
select body_mass_g
from penguins
where
    body_mass_g > (
        select avg(body_mass_g)
        from penguins
    )
limit 5;
```
![query46](screeny/query46.png)

### Exercise 14 
Use a subquery to find the number of penguins that weigh the same as the lightest penguin.
```bash
SELECT COUNT(*) AS number_of_penguins
FROM penguins
WHERE body_mass_g = (SELECT MIN(body_mass_g) FROM penguins);
```
![exercise](screeny/exercise14.png)

### 47. Comparing Individual Values to Aggregates Within Groups
```bash
select
    penguins.species,
    penguins.body_mass_g,
    round(averaged.avg_mass_g, 1) as avg_mass_g
from penguins inner join (
    select
        species,
        avg(body_mass_g) as avg_mass_g
    from penguins
    group by species
) as averaged
    on penguins.species = averaged.species
where penguins.body_mass_g > averaged.avg_mass_g
limit 5;
```
![query47](screeny/query47.png)

### Exercise 15
Use a subquery to find the number of penguins that weigh the same as the lightest penguin of the same sex and species.
```bash
SELECT COUNT(*) AS number_of_penguins
FROM penguins
WHERE body_mass_g = (SELECT MIN(body_mass_g) FROM penguins) AND species = (SELECT species FROM penguins WHERE body_mass_g = (SELECT MIN(body_mass_g) FROM penguins)) AND sex = (SELECT sex FROM penguins WHERE body_mass_g = (SELECT MIN(body_mass_g) FROM penguins));
```
![exercise15](screeny/exercise15.png)


### 48. Common Table Expressions
```bash
with grouped as (
    select
        species,
        avg(body_mass_g) as avg_mass_g
    from penguins
    group by species
)

select
    penguins.species,
    penguins.body_mass_g,
    round(grouped.avg_mass_g, 1) as avg_mass_g
from penguins inner join grouped
where penguins.body_mass_g > grouped.avg_mass_g
limit 5;
```
![query48](screeny/query48.png)


### 49. Explaining Query Plans
```bash
explain query plan
select
    species,
    avg(body_mass_g)
from penguins
group by species;
```
![query49](screeny/query49.png)

### Exercise 16
Use a CTE to find the number of penguins that weigh the same as the lightest penguin of the same sex and species.
```bash
WITH LightestPenguins AS (
    SELECT species, sex, MIN(body_mass_g) AS min_weight
    FROM penguins
    GROUP BY species, sex
)
SELECT p.species, p.sex, COUNT(*) AS number_of_penguins
FROM penguins p
JOIN LightestPenguins lp
ON p.species = lp.species AND p.sex = lp.sex AND p.body_mass_g = lp.min_weight
GROUP BY p.species, p.sex;
```
![exercise16](screeny/exercise16.png)


### 50. Enumerating Rows
```bash
select
    rowid,
    species,
    island
from penguins
limit 5;
```
![query50](screeny/query50.png)

### Exercise 17
```bash
CREATE TABLE test_table (
    value TEXT
);

INSERT INTO test_table (value) VALUES ('Row1');
INSERT INTO test_table (value) VALUES ('Row2');
INSERT INTO test_table (value) VALUES ('Row3');

SELECT rowid, value FROM test_table;
```
![exercise17p1](screeny/exercise17p1.png)
```bash
DELETE FROM test_table;

INSERT INTO test_table (value) VALUES ('Row1');
INSERT INTO test_table (value) VALUES ('Row2');
INSERT INTO test_table (value) VALUES ('Row3');

SELECT rowid, value FROM test_table;
```
![exercise17p2](screeny/exercise17p2.png)

### 51. Conditionals
```bash
with sized_penguins as (
    select
        species,
        iif(
            body_mass_g < 3500,
            'small',
            'large'
        ) as size
    from penguins
    where body_mass_g is not null
)

select
    species,
    size,
    count(*) as num
from sized_penguins
group by species, size
order by species, num;
```
![query51](screeny/query51.png)

### Exercise 18
How does the result of the previous query change if the check for null body mass is removed? Why is the result without that check misleading?

What does each of the expressions shown below produce? Which ones do you think actually attempt to divide by zero?
iif(0, 123, 1/0)
iif(1, 123, 1/0)
iif(0, 1/0, 123)
iif(1, 1/0, 123)
```bash
with sized_penguins as (
    select
        species,
        iif(
            body_mass_g < 3500,
            'small',
            'large'
        ) as size
    from penguins
    where body_mass_g 
)

select
    species,
    size,
    count(*) as num
from sized_penguins
group by species, size
order by species, num;
```
![exercise18p1](screeny/exercise18p1.png)
```bash

SELECT iif(0, 123, 1/0) AS result;

```
![exercise18p2](screeny/exercise18p2.png)
```bash
SELECT iif(1, 123, 1/0) AS result;
```
![exercise18p3](screeny/exercise18p3.png)

```bash
SELECT iif(0, 1/0, 123) AS result;
```
![exercise18p4](screeny/exercise18p4.png)
```bash

SELECT iif(1, 1/0, 123) AS result;

```
![exercise18p5](screeny/exercise18p5.png)

### 52.Selecting a Case
```bash
with sized_penguins as (
    select
        species,
        case
            when body_mass_g < 3500 then 'small'
            when body_mass_g < 5000 then 'medium'
            else 'large'
        end as size
    from penguins
    where body_mass_g is not null
)

select
    species,
    size,
    count(*) as num
from sized_penguins
group by species, size
order by species, num;
```
![query52](screeny/query52.png)

### Exercise 19
Modify the query above so that the outputs are "penguin is small" and "penguin is large" by concatenating the string "penguin is " to the entire case rather than to the individual when branches. (This exercise shows that case/when is an expression rather than a statement.)
```bash
with sized_penguins as (
    select
        species,
        'penguin is ' || case
            when body_mass_g < 3500 then 'small'
            when body_mass_g < 5000 then 'medium'
            else 'large'
        end as size
    from penguins
    where body_mass_g is not null
)

select
    species,
    size,
    count(*) as num
from sized_penguins
group by species, size
order by species, num;
```
![exercise19](screeny/exercise19.png)

### 53. Checking a Range
```bash
with sized_penguins as (
    select
        species,
        case
            when body_mass_g between 3500 and 5000 then 'normal'
            else 'abnormal'
        end as size
    from penguins
    where body_mass_g is not null
)

select
    species,
    size,
    count(*) as num
from sized_penguins
group by species, size
order by species, num;
```
![query53](screeny/query53.png)

### Exercise 20
The expression val between 'A' and 'Z' is true if val is 'M' (upper case) but false if val is 'm' (lower case). Rewrite the expression using SQLite's built-in scalar functions so that it is true in both cases.
```bash
SELECT UPPER(val) BETWEEN 'A' AND 'Z';
```
![exercise20p1](screeny/exercise20p1.png)
![exercise20p2](screeny/exercise20p2.png)

### 54. Yet Another Database
```bash
select * from staff;
```
![query54](screeny/query54.png)

### 55. Pattern Matching
```bash
select
    personal,
    family
from staff
where personal like '%ya%';
```
![query55](screeny/query55.png)

### Exercise 21
Rewrite the pattern-matching query shown above using glob.
```bash
select
    personal,
    family
from staff
where personal glob '*ya*';
```
![exercise21](screeny/exercise21.png)

### 56. Selecting First and Last Rows
```bash
select * from (
    select * from (select * from experiment order by started asc limit 5)
    union all
    select * from (select * from experiment order by started desc limit 5)
)
order by started asc;
```
![query56](screeny/query56.png)

### Exercise 22
```bash
SELECT *
FROM penguins
WHERE species = 'Adelie'
UNION ALL
SELECT *
FROM penguins
WHERE species = 'Adelie' ORDER BY bill_depth_mm;
```
![exercise22p1](screeny/exercise22p1.png)
```bash
SELECT *
FROM penguins
WHERE species = 'Adelie' ORDER BY bill_depth_mm;
```
![exercise22p2](screeny/exercise22p2.png)

### 57. Intersection
```bash
select
    personal,
    family,
    dept,
    age
from staff
where dept = 'mb'
intersect
select
    personal,
    family,
    dept,
    age from staff
where age < 50;
```
![query57](screeny/query57.png)

### Exercise 23
```bash
SELECT *
FROM penguins
WHERE species = 'Adelie'
INTERSECT
SELECT *
FROM penguins
WHERE body_mass_g > 4000;
```
![exercise23p1](screeny/exercise23p1.png)
```bash
SELECT *
FROM penguins
WHERE species = 'Adelie' AND body_mass_g > 4000;
```
![exercise23p2](screeny/exercise23p2.png)
```bash
EXPLAIN QUERY PLAN
SELECT *
FROM penguins
WHERE species = 'Adelie'
INTERSECT
SELECT *
FROM penguins
WHERE body_mass_g > 4000;
```
![exercise23p3](screeny/exercise23p3.png)
```bash
EXPLAIN QUERY PLAN
SELECT *
FROM penguins
WHERE species = 'Adelie' AND body_mass_g > 4000;
```
![exercise23p4](screeny/exercise23p4.png)

Using 'WHERE' seems more efficient because it is faster and less complicated.

### 58. Exclusion
```bash
select
    personal,
    family,
    dept,
    age
from staff
where dept = 'mb'
except
    select
        personal,
        family,
        dept,
        age from staff
    where age < 50;
```
![query58](screeny/query58.png)

### Exercise 24
Use exclude to find all Gentoo penguins that aren’t male. How can you check that your query is working correctly?
```bash
SELECT *
FROM penguins
WHERE species = 'Gentoo'
EXCEPT
SELECT *
FROM penguins
WHERE species = 'Gentoo' AND sex = 'Male';
```
![exercise24p1](screeny/exercise24p1.png)
Check:
```bash

```
![exercise24p2](screeny/exercise24p2.png)

### 59. Random Numbers and Why Not
```bash
with decorated as (
    select random() as rand,
    personal || ' ' || family as name
    from staff
)

select
    rand,
    abs(rand) % 10 as selector,
    name
from decorated
where selector < 5;
```
![query59](screeny/query59.png)

### Exercise 25
Write a query that:

uses a CTE to create 1000 random numbers between 0 and 10 inclusive;

uses a second CTE to calculate their mean;
```bash
WITH RECURSIVE random_numbers AS (
    SELECT RANDOM() % 11 AS value
    UNION ALL
    SELECT RANDOM() % 11
    FROM random_numbers
    LIMIT 1000
),
mean_value AS (
    SELECT AVG(value) AS mean
    FROM random_numbers
),
variance AS (
    SELECT AVG((value - mean_value.mean) * (value - mean_value.mean)) AS var
    FROM random_numbers, mean_value
)
SELECT mean_value.mean
FROM mean_value;

```
![exercise25](screeny/exercise25.png)

### 60. Creating an Index
```bash
explain query plan
select filename
from plate
where filename like '%07%';
```
![query60](screeny/query60.png)

### 61.Self Join
```bash
with person as (
    select
        ident,
        personal || ' ' || family as name
    from staff
)

select
    left_person.name,
    right_person.name
from person as left_person inner join person as right_person
limit 10;
```
![query61](screeny/query61.png)

### 62. Generating Unique Pairs
```bash
with person as (
    select
        ident,
        personal || ' ' || family as name
    from staff
)

select
    left_person.name,
    right_person.name
from person as left_person inner join person as right_person
on left_person.ident < right_person.ident
where left_person.ident <= 4 and right_person.ident <= 4;
```
![query62](screeny/query62.png)

### 63. Filtering Pairs
```bash
with
person as (
    select
        ident,
        personal || ' ' || family as name
    from staff
),

together as (
    select
        left_perf.staff as left_staff,
        right_perf.staff as right_staff
    from performed as left_perf inner join performed as right_perf
        on left_perf.experiment = right_perf.experiment
    where left_staff < right_staff
)

select
    left_person.name as person_1,
    right_person.name as person_2
from person as left_person inner join person as right_person join together
    on left_person.ident = left_staff and right_person.ident = right_staff;
```
![query63](screeny/query63.png)

### 64. Existence and Correlated Subqueries
```bash
select
    name,
    building
from department
where
    exists (
        select 1
        from staff
        where dept = department.ident
    )
order by name;
```
![query64](screeny/query64.png)

### 65. Nonexistence
```bash
select
    name,
    building
from department
where
    not exists (
        select 1
        from staff
        where dept = department.ident
    )
order by name;
```
![query65](screeny/query65.png)

### Exercise 26
Can you rewrite the previous query using exclude? If so, is your new query easier to understand? If the query cannot be rewritten, why not?
```bash
SELECT
    department.name,
    department.building
FROM department
LEFT JOIN staff ON department.ident = staff.dept
WHERE staff.dept IS NULL
ORDER BY department.name;
```
In my opinion, this query is easier to understand for less advanced users.

![exercise26](screeny/exercise26.png)


### 66. Avoiding Correlated Subqueries
```bash
select distinct
    department.name as name,
    department.building as building
from department inner join staff
    on department.ident = staff.dept
order by name;
```
![query66](screeny/query66.png)

### 67. Lead and Lag
```bash
with ym_num as (
    select
        strftime('%Y-%m', started) as ym,
        count(*) as num
    from experiment
    group by ym
)

select
    ym,
    lag(num) over (order by ym) as prev_num,
    num,
    lead(num) over (order by ym) as next_num
from ym_num
order by ym;
```
![query67](screeny/query67.png)


### 68. Windowing Functions
```bash
with ym_num as (
    select
        strftime('%Y-%m', started) as ym,
        count(*) as num
    from experiment
    group by ym
)

select
    ym,
    num,
    sum(num) over (order by ym) as num_done,
    (sum(num) over (order by ym) * 1.00) / (select sum(num) from ym_num) as completed_progress,
    cume_dist() over (order by ym) as linear_progress
from ym_num
order by ym;
```
![query68](screeny/query68.png)

### 69. Explaining Another Query Plan
```bash
explain query plan
with ym_num as (
    select
        strftime('%Y-%m', started) as ym,
        count(*) as num
    from experiment
    group by ym
)
select
    ym,
    num,
    sum(num) over (order by ym) as num_done,
    cume_dist() over (order by ym) as progress
from ym_num
order by ym;
```
![query69](screeny/query69.png)


### 70. Partitioned Windows
```bash
with y_m_num as (
    select
        strftime('%Y', started) as year,
        strftime('%m', started) as month,
        count(*) as num
    from experiment
    group by year, month
)

select
    year,
    month,
    num,
    sum(num) over (partition by year order by month) as num_done
from y_m_num
order by year, month;
```
![query70](screeny/query70.png)

### Exercise 27
Create a query that:

finds the unique weights of the penguins in the penguins database;

sorts them;

finds the difference between each successive distinct weight; and

counts how many times each unique difference appears.
```bash
WITH sorted_weights AS (
    SELECT DISTINCT body_mass_g
    FROM penguins
    WHERE body_mass_g IS NOT NULL
    ORDER BY body_mass_g
),
differences AS (
    SELECT 
        body_mass_g,
        LAG(body_mass_g) OVER (ORDER BY body_mass_g) AS prev_weight
    FROM sorted_weights
),
calculated_diffs AS (
    SELECT 
        body_mass_g - prev_weight AS diff
    FROM differences
    WHERE prev_weight IS NOT NULL
)
SELECT 
    diff,
    COUNT(*) AS count
FROM calculated_diffs
GROUP BY diff
ORDER BY count DESC;
```
![exercise27](screeny/exercise27.png)

### 71. Storing JSON
```bash
select * from machine;
```
![query71](screeny/query71.png)

### 72. Unpacking JSON Arrays
```bash
select
    ident,
    json_each.key as key,
    json_each.value as value
from usage, json_each(usage.log)
limit 10;
```
![query72](screeny/query72.png)

### 73. Modifying JSON
```bash
select
    ident,
    name,
    json_set(details, '$.sold', json_quote('2024-01-25')) as updated
from machine;
```
![query73](screeny/query73.png)

### 74. Refreshing the Penguins Database
```bash
select
    species,
    count(*) as num
from penguins
group by species;
```
![query74](screeny/query74.png)

### 75. Tombstones
```bash
alter table penguins
add active integer not null default 1;

update penguins
set active = iif(species = 'Adelie', 0, 1);
select
    species,
    count(*) as num
from penguins
where active
group by species;
```
![query75](screeny/query75.png)

### 76. Hours Reminder
```bash
create table job (
    name text not null,
    billable real not null
);
insert into job values
('calibrate', 1.5),
('clean', 0.5);
select * from job;
```
![query](screeny/query.png)

### 77. Adding Checks
```bash
create table job (
    name text not null,
    billable real not null,
    check (billable > 0.0)
);
insert into job values ('calibrate', 1.5);
insert into job values ('reset', -0.5);
```
![query77p1](screeny/query77p1.png)
```bash
select * from job;
```
![query77p2](screeny/query77p2.png)

### Exercise 28
Rewrite the definition of the penguins table to add the following constraints:

body_mass_g must be null or non-negative.

island must be one of "Biscoe", "Dream", or "Torgersen". (Hint: the in operator will be useful here.)
```bash
CREATE TABLE penguins (
    species TEXT,
    island TEXT CHECK (island IN ('Biscoe', 'Dream', 'Torgersen')),
    bill_length_mm REAL,
    bill_depth_mm REAL,
    flipper_length_mm REAL,
    body_mass_g REAL CHECK (body_mass_g IS NULL OR body_mass_g >= 0),
    sex TEXT
);

INSERT INTO penguins VALUES('Adelie','Dreayy',39.60000000000000142,18.10000000000000143,186.0,4450.0,'MALE');
```
![exercise28](screeny/exercise28.png)

### 78. Transactions
```bash
create table job (
    name text not null,
    billable real not null,
    check (billable > 0.0)
);

insert into job values ('calibrate', 1.5);

begin transaction;
insert into job values ('clean', 0.5);
rollback;

select * from job;
```
![query78](screeny/query78.png)

### 79. Rollback in Constraints
```bash
create table job (
    name text not null,
    billable real not null,
    check (billable > 0.0) on conflict rollback
);

insert into job values
    ('calibrate', 1.5);
insert into job values
    ('clean', 0.5),
    ('reset', -0.5);
```
![query79](screeny/query79.png)
```bash
select * from job;
```
![query79p2](screeny/query79p2.png)

### 80. Rollback in Statements
```bash
create table job (
    name text not null,
    billable real not null,
    check (billable > 0.0)
);

insert or rollback into job values
('calibrate', 1.5);
insert or rollback into job values
('clean', 0.5),
('reset', -0.5);
```
![query80p1](screeny/query80p1.png)
```bash
select * from job;
```
![query80p2](screeny/query80p2.png)

### 81. Upsert
```bash
create table jobs_done (
    person text unique,
    num integer default 0
);

insert into jobs_done values
('zia', 1);
.print 'after first'
select * from jobs_done;
.print


insert into jobs_done values
('zia', 1);
.print 'after failed'
```
![query81p1](screeny/query81p1.png)
```bash
select * from jobs_done;
```
![query81p2](screeny/query81p2.png)
```bash
insert into jobs_done values
('zia', 1)
on conflict(person) do update set num = num + 1;
.print '\nafter upsert'
select * from jobs_done;
```
![query81p3](screeny/query81p3.png)

### 82. Creating Triggers
```bash
-- Track hours of lab work.
create table job (
    person text not null,
    reported real not null check (reported >= 0.0)
);

-- Explicitly store per-person total rather than using sum().
create table total (
    person text unique not null,
    hours real
);

-- Initialize totals.
insert into total values
('gene', 0.0),
('august', 0.0);

-- Define a trigger.
create trigger total_trigger
before insert on job
begin
    -- Check that the person exists.
    select case
        when not exists (select 1 from total where person = new.person)
        then raise(rollback, 'Unknown person ')
    end;
    -- Update their total hours (or fail if non-negative constraint violated).
    update total
    set hours = hours + new.reported
    where total.person = new.person;
end;
```
![query82](screeny/query82.png)

### 83. Trigger Not Firing
```bash
insert into job values
('gene', 1.5),
('august', 0.5),
('gene', 1.0);

SELECT * FROM job;
```
![query83](screeny/query83.png)

### 84. Trigger Firing
```bash
insert into job values
('gene', 1.0),
('august', -1.0);
```
![query84](screeny/query84.png)

### Exercise 30
Using the penguins database:

create a table called species with columns name and count; and

define a trigger that increments the count associated with each species each time a new penguin is added to the penguins table.

Does your solution behave correctly when several penguins are added by a single insert statement?
```bash
CREATE TABLE species (
    name TEXT PRIMARY KEY,
    count INTEGER DEFAULT 0
);

CREATE TRIGGER increment_species_count
AFTER INSERT ON penguins
FOR EACH ROW
BEGIN
    INSERT INTO species (name, count)
    VALUES (NEW.species, 1)
    ON CONFLICT(name) DO UPDATE SET count = count + 1;
END;

INSERT INTO penguins (species, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex)
VALUES 
    ('Adelie', 'Biscoe', 39.1, 18.7, 181, 3750, 'male'),
    ('Chinstrap', 'Dream', 50.5, 19.3, 194, 4200, 'female'),
    ('Adelie', 'Biscoe', 40.3, 20.1, 190, 3800, 'female');

SELECT * FROM species;

```
![exercise30](screeny/exercise30.png)

### 85. Representing Graphs
```bash
create table lineage (
    parent text not null,
    child text not null
);
insert into lineage values
('Arturo', 'Clemente'),
('Darío', 'Clemente'),
('Clemente', 'Homero'),
('Clemente', 'Ivonne'),
('Ivonne', 'Lourdes'),
('Soledad', 'Lourdes'),
('Lourdes', 'Santiago');
select * from lineage;
```
![query85](screeny/query85.png)

### exercise 31
Write a query that uses a self join to find every person's grandchildren.
```bash
SELECT DISTINCT
    grandparent.parent AS grandparent,
    grandchild.child AS grandchild
FROM
    lineage AS parent
JOIN
    lineage AS grandparent ON parent.parent = grandparent.child
JOIN
    lineage AS grandchild ON parent.child = grandchild.parent;
```
![exercise31](screeny/exercise31.png)

### 86. Recursive Queries
```bash
with recursive descendent as (
    select
        'Clemente' as person,
        0 as generations
    union all
    select
        lineage.child as person,
        descendent.generations + 1 as generations
    from descendent inner join lineage
        on descendent.person = lineage.parent
)

select
    person,
    generations
from descendent;
```
![query86](screeny/query86.png)

### Exercise 32
```bash
with recursive descendent as (
    select
        'Clemente' as person,
        0 as generations
    union
    select
        lineage.child as person,
        descendent.generations + 1 as generations
    from descendent inner join lineage
        on descendent.person = lineage.parent
)

select
    person,
    generations
from descendent;
```
![exercise32](screeny/exercise32.png)
The result from union is the same because there are no duplicates in the table

### 87. Contact Tracing Database
```bash
select * from person;
```
![query87p1](screeny/query87p1.png)
```bash
select * from contact;
```
![query87p2](screeny/query87p2.png)

### 88. Bidirectional Contacts
```bash
create temporary table bi_contact (
    left text,
    right text
);

insert into bi_contact
select
    left, right from contact
    union all
    select right, left from contact
;

SELECT*FROM bi_contact;
```
![query88](screeny/query88.png)

### 89. Updating Group Identifiers
```bash
select
    left.name as left_name,
    left.ident as left_ident,
    right.name as right_name,
    right.ident as right_ident,
    min(left.ident, right.ident) as new_ident
from
    (person as left join bi_contact on left.name = bi_contact.left)
    join person as right on bi_contact.right = right.name;
```
![query89](screeny/query89.png)

### 90. Recursive Labeling
```bash
with recursive labeled as (
    select
        person.name as name,
        person.ident as label
    from
        person
    union -- not 'union all'
    select
        person.name as name,
        labeled.label as label
    from
        (person join bi_contact on person.name = bi_contact.left)
        join labeled on bi_contact.right = labeled.name
    where labeled.label < person.ident
)
select name, min(label) as group_id
from labeled
group by name
order by label, name;
```
![query90](screeny/query90.png)

### Exercise 33
Modify the query above to use union all instead of union to trigger infinite recursion. How can you modify the query so that it stops at a certain depth so that you can trace its output?
```bash
with recursive labeled as (
    select
        person.name as name,
        person.ident as label
    from
        person
    union ALL
    select
        person.name as name,
        labeled.label as label
    from
        (person join bi_contact on person.name = bi_contact.left)
        join labeled on bi_contact.right = labeled.name
    where labeled.label < person.ident
	AND labeled.depth < 5  
)
select name, min(label) as group_id
from labeled
group by name
order by label, name;
```
![exercise33](screeny/exercise33.png)

I added a stopping condition at depth level 5

