
Select 
*
from (
    Select 
        "Country Name"
        ,Year
        ,Value/1000000 as CurrentGDPinM
        ,(Value/ValuePrev - 1)*100 as GDPChangeInPrcnt
        ,row_number() over (partition by "Country Name" order by Year desc) as chekk  
    from (
        Select 
            "Country Name", Year, Value, 
            lag(Value) over (partition by "Country Name" order by Year) as ValuePrev
                
        from gdp 
    ) a
    where ValuePrev not null 
) b 
where chekk = 1;
