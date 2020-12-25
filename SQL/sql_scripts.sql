-- 
--	employees: employee_id, first_name, last_name, hire_date, salary, manager_id, department_id
--	departments: department_id, department_name, location_id
-- We would like to know for each department top earning employee, salary, difference from the second earning employee


-- 

WITH emp_dep as (
select employee_id,first_name, last_name, hire_date, salary, manager_id, department_id,	department_name, location_id,
row_number() over (partition by department order by salary desc) as rank
from employees emp inner join department dep on emp.department_id = dep.department_id
),
emp_dep_first_second_salary AS (
select 				
				department_name ,
				location_id, 
				if(rank = 1, salary,null) as top_salary,
				if(rank = 2 , second_salary , null)  second_salary
from emp_dep 
) 
select department_name , location_id , (top_salary - second_salary) as DIFF_Sallery
from emp_dep_first_second_salary 
where top_salary is not null or second_salary is not null;


--
--	site_visitors : date, site, number of visitors 
--	promotion dates : start_date, end_date, site, promotion_code
-- 
-- We would like to know what percent of the site traffic was on promotion dates 

with all_sites_in_promotion_dates as (
select * 
from promotion inner join site_visitors using (site) 
where date between start_date and end_date 
)
select sumif(in_promotion.number_of_visitors)*100/sum(all_sites.number_of_visitors) as  percent_of_the_site_traffic_on_on promotion_dates 
from all_sites_in_promotion_dates in_promotion join sites all_sites on (site);



