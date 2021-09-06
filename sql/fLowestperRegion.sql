Select "Country Name", region, Value/1000000 GDPValue

From 
(
    Select *, base.region,
    row_number() over (partition by GDP.Year, base.region order by gdp.Value asc) as chekk
    from GDP
    left join base on gdp."Country Code" = base.id
    where GDP.Year = 2017

) a
where a.chekk < 4
and 
order by region;