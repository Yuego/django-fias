WITH RECURSIVE PATH (docid, aoguid, aolevel, scname, fullname) AS (
  SELECT NEXTVAL('fias_addrobj_id_seq') AS docid, ao.aoguid, ao.aolevel,
    (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao.shortname AND sn.level=ao.aolevel)::TEXT AS scname,
    ao.shortname || ' ' || formalname AS fullname
  FROM fias_addrobj AS ao
  WHERE aolevel = 1 AND livestatus = TRUE
  UNION
  SELECT NEXTVAL('fias_addrobj_id_seq') AS docid, child.aoguid, child.aolevel,
    PATH.scname::TEXT || ', ' || (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=child.shortname AND sn.level=child.aolevel) AS scname,
    PATH.fullname || ', ' || child.shortname || ' ' || child.formalname AS fullname
  FROM fias_addrobj AS child, PATH
  WHERE child.parentguid = PATH.aoguid AND livestatus = TRUE
)
SELECT * FROM PATH;
