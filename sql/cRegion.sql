Select

region, sum(case when incomeLevel = 'High income' then 1 else 0 end) / sum(1) as proportion

from base

order by 2 desc
limit 1;
