import sqlglot
import networkx as nx
import matplotlib.pyplot as plt
from sqlglot import exp


#Creating Global dag



#node for table/cte/view/subquery
class Querynode:

    def __init__(self,name,node_type,select_columns = None,join_condition = None,where_condition = None,group_by = None):
        self.name  = name
        self.node_type = node_type
        self.select_columns  = select_columns or []
        self.join_condition = join_condition or []
        self.where_condition = where_condition or []
        self.group_by = group_by or []
        self.edges = [] 
    def add_adge(node):
        self.edges.append(node)

    def __repr__(self):
        return f"{self.node_type}({self.name})"
        


def extract_node(sql_query):

    parsed_query = sqlglot.parse_one(sql_query)

    nodes = {}

    def traverse(node):
       
        if isinstance(node, exp.Table):  # Table node
            print("table")
            table_name = node.name
            nodes[table_name] = Querynode(name=table_name, node_type="Table")
        elif  isinstance(node,exp.With):
            print("with")
            for cte in node.expression:
                cte_name =  cte.alias_or_name
                nodes[cte_name] = Querynode(name=cte_name, node_type="CTE")
                

        elif isinstance(node,exp.Subquery):
            print("sub")
            sub_query_name  = node.alias_or_name or f"subquery_{len(nodes)}"
            nodes[sub_query_name] = Querynode(name=sub_query_name, node_type="Subquery")
            traverse(node)

        elif isinstance(node, exp.Join):  # Join conditions
            print("join")
            left_table = node.left.alias_or_name
            right_table = node.right.alias_or_name
            condition = node.args.get("on")
            if left_table in nodes and right_table in nodes:
                nodes[left_table].add_edge(nodes[right_table])
                nodes[right_table].add_edge(nodes[left_table])
                nodes[left_table].join_conditions.append(str(condition))
        for child in node.args.values():
            print("\n\n\n "+str(child)+str(type(child)))
           
            if isinstance(child, list) and child != None:
                for sub in child:
                    traverse(sub)
            elif isinstance(child, exp.Expression) and child != None:
                traverse(child)
    nodes = traverse(parsed_query)
    print(nodes)
    return nodes



    
    


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


root  = extract_node("select * from tree")

