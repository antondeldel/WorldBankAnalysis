
Select 
    a.region, a.incomeLevel, a.name
    , sum(Value) over (partition by a.region order by b.OrderID, a.name)/1000000 RollingSumM 

From gdp 
left join base a on gdp."Country Code" = a.id 
left join 
        (
        Select 'Low income' as incomeLevel, 1 as OrderID

        union all Select 'Upper middle income',2
        union all Select 'Lower middle income',3
        union all Select 'High income',4
        union all Select 'Aggregates', 5

        )  b
    on a.incomeLevel = b.incomeLevel

where a.incomeLevel <> 'Aggregates' and gdp.Year = 2017

order by a.region, b.OrderID, a.name;