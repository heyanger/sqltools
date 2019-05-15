[![Build Status](https://travis-ci.com/funkytennisball/sqltools.svg?branch=master)](https://travis-ci.com/funkytennisball/sqltools)

# SQL tools

This module provides sql to tree parsing as well as edit sequence generation (based on SyntaxSQLNet https://arxiv.org/abs/1810.05237)

## Usage

### Converting a sql into a tree and back
```python
from sqltools.parser import to_tree, to_sql

sql = 'SELECT * FROM table'
tree = to_tree(sql)
parsed = to_sql(tree)
```

### Generating an edit sequence and apply sequence
```python
from sqltools.parser import to_tree, to_sql
from sqltools.sequence import generate_sequence, apply_sequence_sql

sql1 = "SELECT * FROM Owners"
sql2 = "SELECT count(*) FROM Owners WHERE state = 'Arizona'"

# SQL based
sequence = generate_sequence_sql(sql1, sql2)
assert(apply_sequence_sql(sql1, sequence) == sql2)

# Tree based
sequence = generate_sequence(to_tree(sql1), to_tree(sql2))
assert(to_sql(apply_sequence(to_tree(sql1), sequence)) == sql2)
```

## Queries not supported
- Nested Queries in FROM i.e. `SELECT * FROM (SELECT * FROM table)`
- JOIN not supported
- complex AND/OR queries