sql_get_clients = """
select cl.ID, cl.Name as client,
GROUP_CONCAT( p.ID) as projectID, 
GROUP_CONCAT( p.Title) as projectName       
 from  
    (select * from projects {projectCondition}) p  
INNER JOIN
(select * from clients {clientCondition}) cl
ON cl.ID = p.Client_ID 
group by cl.Name,cl.ID
"""

sql_get_cost_group = """
select a.ID as mainCostID, a.Name,b.Name as subCostName,b.ID as subCostID from 
(select * from cost_types ) a 
join 
(select * from cost_types) b
on a.id = b.Parent_Cost_Type_ID
"""

sql_get_project_cost = """
SELECT 
	   c.ID as Client_ID,
       c.Name as Client_Name,
       p.ID as Project_ID,
       p.Title,
       ct.Name,
       cs.Amount,
       IF(isnull(Parent_Cost_Type_ID),0 ,Parent_Cost_Type_ID) as Parent_Cost_Type_ID,
       ct.ID as Cost_Type_ID
FROM  ( select * from projects {projectCondition}) p  
JOIN costs cs ON (cs.Project_ID=p.ID)
JOIN (select * from cost_types {costTypeCondition}) ct ON (ct.ID=cs.Cost_Type_ID)
JOIN (select * from clients {clientCondition}) c ON c.ID = p.Client_ID
 
"""

sql_get_cost_child = """
select count(ID) as Total ,IF(isnull(Parent_Cost_Type_ID),0 ,Parent_Cost_Type_ID) as Parent_ID from cost_types group by Parent_Cost_Type_ID;
"""