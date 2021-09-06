

Select 
"Country Name", Year,Value/1000000 as CurrentGDPinM, (Value/ValuePrev - 1)*100 as GDPChangeInPrcnt  
from (
Select 
"Country Name", Year, Value, 
lag(Value) over (partition by "Country Name" order by Year) as ValuePrev
from gdp ) a
where ValuePrev not null

limit 10;