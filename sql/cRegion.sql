Select

region, sum(case when incomeLevel = 'High income' then 1.00 else 0.00 end) / sum(1.00) as proportion

from base

group by region
order by 2 desc
limit 1;
