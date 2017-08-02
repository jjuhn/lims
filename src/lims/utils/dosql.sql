select count(*) from disease_ontology;

select count(distinct(name)) from disease_ontology;


select name from disease_ontology group by name having count(*) >1

select count(*) from disease_ontology where not deprecated ;

select description from synonym group by description having count(*) >1 ;



select d_o.id, d_o.name, syn.description, syn.scope, d_o.deprecated
from disease_ontology d_o
  inner join do_synonym ds on ds.do_id = d_o.id
  inner join synonym syn on syn.id = ds.syn_id
where ds.syn_id in (select syn_id from do_synonym group by syn_id having count(*) >1) order by ds.syn_id



--where syn.description like '%Parkinson%';




select
  p.id as "phenotype ID",
  p.name as "phenotype Name",
  o.id as "OMIM ID",
  o.name as "OMIM Name",
  d.name as "Disease Ontology Name"
-- count(*)
from phenotype_ontology p
inner join pheno_omim po on po.phenotype_id = p.id
inner join omim o on o.id = po.omim_id
inner join do_omim doo on doo.omim_id = o.id
inner join disease_ontology d on d.id = doo.do_id
where p.name like '%arkinson%'
 ;
-- where p.name like '%atigue%';






-- where p.name like '%Supranuclear gaze palsy%'


select count(*) from disease_ontology;




select * from disease_ontology d
inner join do_omim doo on doo.do_id = d.id

select count(*) from do_omim;
select count(*) from pheno_omim;


select DISTINCT omim_id from do_omim
intersect
select DISTINCT omim_id from pheno_omim;





select DISTINCT omim_id from do_omim;



select DISTINCT omim_id from pheno_omim;




select * from disease_ontology where id = 863;




select * from phenotype where id = 2167;





-- left outer join do_omim doo on doo.omim_id = o.id
-- left outer join disease_ontology d on d.id = doo.do_id
--
-- where p.name like '%adykinesia%'



select * from phenotype_ontology po
inner join po_synonym pos on pos.po_id = po.id
inner join synonym syn on syn.id = pos.syn_id
where po.id = 11945

;


select * from synonym where description like '%neumonia%';






select * from po_synonym where syn_id = 35421;




select * from omim where omim.qualifier is not null;



select
  po.id,
  po.name,
  po.namespace,
  po.deprecated,
  po.xref,
  po.hasalternativeid,
  po.description,
  r.p_id
from phenotype_ontology po
left outer join po_relationship r on r.c_id = po.id order by po.id;




select count(*) FROM omim WHERE morbid_name IS NOT NULL;

select count(*) from omim where name is null and morbid_name is null;



select * from omim;
