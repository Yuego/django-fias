WITH RECURSIVE PATH (docid, aoguid, aolevel, scname, fullname, item_weight) AS (
  SELECT DISTINCT ON (ao.aoguid) NEXTVAL('fias_addrobj_docid_seq') AS docid, ao.aoguid, ao.aolevel,
    sn.socrname::TEXT AS scname,
    ao.shortname || ' ' || formalname AS fullname,
    sn.item_weight
  FROM fias_addrobj AS ao
    INNER JOIN fias_socrbase AS sn ON (sn.scname = ao.shortname AND sn.level = ao.aolevel)
  WHERE aolevel = 1 AND livestatus = TRUE
  UNION
  SELECT DISTINCT ON (child.aoguid) NEXTVAL('fias_addrobj_docid_seq') AS docid, child.aoguid, child.aolevel,
    PATH.scname::TEXT || ', ' || sn.socrname::TEXT AS scname,
    PATH.fullname || ', ' || child.shortname || ' ' || child.formalname AS fullname,
    sn.item_weight
  FROM fias_addrobj AS child
    INNER JOIN fias_socrbase AS sn ON (sn.scname = child.shortname AND sn.level = child.aolevel)
    , PATH
  WHERE child.parentguid = PATH.aoguid AND livestatus = TRUE
)
SELECT * FROM PATH;
