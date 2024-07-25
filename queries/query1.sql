with latest_trips as (
    select
        region,
        datasource,
        datetime,
        row_number() over (partition by region order by	datetime desc) as rn
    from trips
    where region in ( select region
                    from trips
                    group by region
                    order by COUNT(id) desc
                    limit 2))
select
	region,
	datasource,
	datetime
from latest_trips
where rn = 1;
