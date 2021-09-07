interestingFactSQL = '''
Select base.region,
Year,
sum(gdp.Value) Value
from GDP
left join base on gdp."Country Code" = base.id
where base.region <> 'Aggregates'
group by base.region, Year;
'''