import sqlglot
import networkx as nx
import matplotlib.pyplot as plt
from sqlglot import exp


#Creating Global dag

class dag:

    def __init__(self,data,children):
        self.data = data
        self.children = children or []
    
        


def get_dag(parsed):
    print(type(parsed))



sql_query = """
WITH cte AS (
    SELECT id, name FROM users WHERE age > 21
)
SELECT 
    u.id, 
    u.name, 
    o.amount, 
    (SELECT tt FROM cake LIMIT 1) AS subquery_value
FROM cte u
JOIN orders o ON u.id = o.user_id
WHERE o.amount > 100;
"""


parsed = sqlglot.parse_one("select * from cht")

get_dag(parsed)