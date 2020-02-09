SELECT p0.id,
       p0.code,
       p0.title,
       p0.pub_date,
       p0.effective_date,
       p0.note_date,
       p0.dispatch,
       ifnull(re.name, '')            as region,
       e.name                         as effective,
       pr.name                        as property,
       r.name                         as level,
       p0.sub_database,
       p0.content,
       ks.keywords,
       `is`.institutions,
       ts.tags,
       UNIX_TIMESTAMP(p0.update_time) as unix_ts_in_secs
from policy p0
       left join region re on p0.region_id = re.id
       left join effective e on p0.effective_id = e.id
       left join property pr on p0.property_id = pr.id
       left join level r on p0.level_id = r.id
       left join (select ifnull(group_concat(distinct k.name), '') as keywords,
                         p.id
                  from policy p
                         left join keyword_policy kp on kp.policy_id = p.id
                         left join keyword k on kp.keyword_id = k.id
                  group by p.id) ks on ks.id = p0.id
       left join (select ifnull(group_concat(distinct i.name), '') as institutions,
                         p.id
                  from policy p
                         left join institution_policy ip on ip.policy_id = p.id
                         left join institution i on ip.institution_id = i.id
                  group by p.id) `is` on `is`.id = p0.id
       left join (select ifnull(group_concat(distinct t.name), '') as tags, p.id
                  from policy p
                         left join tag_policy tp on tp.policy_id = p.id
                         left join tag t on tp.tag_id = t.id
                  group by p.id) ts on ts.id = p0.id
where (UNIX_TIMESTAMP(p0.update_time) > :sql_last_value AND
       p0.update_time < NOW())
ORDER BY p0.update_time ASC