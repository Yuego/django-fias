INSERT INTO fias_addrobjindex (aoguid, aolevel, scname, fullname, item_weight)

(SELECT DISTINCT (ao.aoguid) AS aoguid,
    ao.aolevel,
    sn.socrname AS scname,
    concat(ao.shortname, " ", ao.formalname) AS fullname,
    sn.item_weight
    FROM fias_addrobj AS ao
      INNER JOIN fias_socrbase AS sn ON (sn.scname = ao.shortname AND sn.level = ao.aolevel)
    WHERE ao.aolevel=1)

UNION

(SELECT DISTINCT (ao2.aoguid) AS aoguid,
    ao2.aolevel,
    concat(sn1.socrname
            , ", ", sn2.socrname
            ) AS scname,
    concat(ao1.shortname, " ", ao1.formalname
            , ", ", ao2.shortname, " ", ao2.formalname
            ) AS fullname,
    sn2.item_weight
    FROM fias_addrobj AS ao1
        INNER JOIN fias_addrobj AS ao2 ON (ao2.parentguid=ao1.aoguid)

        INNER JOIN fias_socrbase AS sn1 ON (sn1.scname = ao1.shortname AND sn1.level = ao1.aolevel)
        INNER JOIN fias_socrbase AS sn2 ON (sn2.scname = ao2.shortname AND sn2.level = ao2.aolevel)
    WHERE ao1.aolevel=1)

UNION

(SELECT DISTINCT (ao3.aoguid) AS aoguid,
    ao3.aolevel,
    concat(sn1.socrname
            , ", ", sn2.socrname
            , ", ", sn3.socrname
            ) AS scname,
    concat(ao1.shortname, " ", ao1.formalname
            , ", ", ao2.shortname, " ", ao2.formalname
            , ", ", ao3.shortname, " ", ao3.formalname
            ) AS fullname,
    sn3.item_weight
    FROM fias_addrobj AS ao1
        INNER JOIN fias_addrobj AS ao2 ON (ao2.parentguid=ao1.aoguid)
        INNER JOIN fias_addrobj AS ao3 ON (ao3.parentguid=ao2.aoguid)

        INNER JOIN fias_socrbase AS sn1 ON (sn1.scname = ao1.shortname AND sn1.level = ao1.aolevel)
        INNER JOIN fias_socrbase AS sn2 ON (sn2.scname = ao2.shortname AND sn2.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn3 ON (sn3.scname = ao3.shortname AND sn3.level = ao3.aolevel)
    WHERE ao1.aolevel=1)

UNION

(SELECT DISTINCT (ao4.aoguid) AS aoguid,
    ao4.aolevel,
    concat(sn1.socrname
            , ", ", sn2.socrname
            , ", ", sn3.socrname
            , ", ", sn4.socrname
            ) AS scname,
    concat(ao1.shortname, " ", ao1.formalname
            , ", ", ao2.shortname, " ", ao2.formalname
            , ", ", ao3.shortname, " ", ao3.formalname
            , ", ", ao4.shortname, " ", ao4.formalname
            ) AS fullname,
    sn4.item_weight
    FROM fias_addrobj AS ao1
        INNER JOIN fias_addrobj AS ao2 ON (ao2.parentguid=ao1.aoguid)
        INNER JOIN fias_addrobj AS ao3 ON (ao3.parentguid=ao2.aoguid)
        INNER JOIN fias_addrobj AS ao4 ON (ao4.parentguid=ao3.aoguid)

        INNER JOIN fias_socrbase AS sn1 ON (sn1.scname = ao1.shortname AND sn1.level = ao1.aolevel)
        INNER JOIN fias_socrbase AS sn2 ON (sn2.scname = ao2.shortname AND sn2.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn3 ON (sn3.scname = ao2.shortname AND sn3.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn4 ON (sn4.scname = ao4.shortname AND sn4.level = ao4.aolevel)
    WHERE ao1.aolevel=1)

UNION

(SELECT DISTINCT (ao5.aoguid) AS aoguid,
    ao5.aolevel,
    concat(sn1.socrname
            , ", ", sn2.socrname
            , ", ", sn3.socrname
            , ", ", sn4.socrname
            , ", ", sn5.socrname
            ) AS scname,
    concat(ao1.shortname, " ", ao1.formalname
            , ", ", ao2.shortname, " ", ao2.formalname
            , ", ", ao3.shortname, " ", ao3.formalname
            , ", ", ao4.shortname, " ", ao4.formalname
            , ", ", ao5.shortname, " ", ao5.formalname
            ) AS fullname,
    sn5.item_weight
    FROM fias_addrobj AS ao1
        INNER JOIN fias_addrobj AS ao2 ON (ao2.parentguid=ao1.aoguid)
        INNER JOIN fias_addrobj AS ao3 ON (ao3.parentguid=ao2.aoguid)
        INNER JOIN fias_addrobj AS ao4 ON (ao4.parentguid=ao3.aoguid)
        INNER JOIN fias_addrobj AS ao5 ON (ao5.parentguid=ao4.aoguid)

        INNER JOIN fias_socrbase AS sn1 ON (sn1.scname = ao1.shortname AND sn1.level = ao1.aolevel)
        INNER JOIN fias_socrbase AS sn2 ON (sn2.scname = ao2.shortname AND sn2.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn3 ON (sn3.scname = ao2.shortname AND sn3.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn4 ON (sn4.scname = ao4.shortname AND sn4.level = ao4.aolevel)
        INNER JOIN fias_socrbase AS sn5 ON (sn5.scname = ao5.shortname AND sn5.level = ao5.aolevel)
    WHERE ao1.aolevel=1)

UNION

(SELECT DISTINCT (ao6.aoguid) AS aoguid,
    ao6.aolevel,
    concat(sn1.socrname
            , ", ", sn2.socrname
            , ", ", sn3.socrname
            , ", ", sn4.socrname
            , ", ", sn5.socrname
            , ", ", sn6.socrname
            ) AS scname,
    concat(ao1.shortname, " ", ao1.formalname
            , ", ", ao2.shortname, " ", ao2.formalname
            , ", ", ao3.shortname, " ", ao3.formalname
            , ", ", ao4.shortname, " ", ao4.formalname
            , ", ", ao5.shortname, " ", ao5.formalname
            , ", ", ao6.shortname, " ", ao6.formalname
            ) AS fullname,
    sn6.item_weight
    FROM fias_addrobj AS ao1
        INNER JOIN fias_addrobj AS ao2 ON (ao2.parentguid=ao1.aoguid)
        INNER JOIN fias_addrobj AS ao3 ON (ao3.parentguid=ao2.aoguid)
        INNER JOIN fias_addrobj AS ao4 ON (ao4.parentguid=ao3.aoguid)
        INNER JOIN fias_addrobj AS ao5 ON (ao5.parentguid=ao4.aoguid)
        INNER JOIN fias_addrobj AS ao6 ON (ao6.parentguid=ao5.aoguid)

        INNER JOIN fias_socrbase AS sn1 ON (sn1.scname = ao1.shortname AND sn1.level = ao1.aolevel)
        INNER JOIN fias_socrbase AS sn2 ON (sn2.scname = ao2.shortname AND sn2.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn3 ON (sn3.scname = ao2.shortname AND sn3.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn4 ON (sn4.scname = ao4.shortname AND sn4.level = ao4.aolevel)
        INNER JOIN fias_socrbase AS sn5 ON (sn5.scname = ao5.shortname AND sn5.level = ao5.aolevel)
        INNER JOIN fias_socrbase AS sn6 ON (sn6.scname = ao6.shortname AND sn6.level = ao6.aolevel)
    WHERE ao1.aolevel=1)

UNION

(SELECT DISTINCT (ao7.aoguid) AS aoguid,
    ao7.aolevel,
    concat(sn1.socrname
            , ", ", sn2.socrname
            , ", ", sn3.socrname
            , ", ", sn4.socrname
            , ", ", sn5.socrname
            , ", ", sn6.socrname
            , ", ", sn7.socrname
            ) AS scname,
    concat(ao1.shortname, " ", ao1.formalname
            , ", ", ao2.shortname, " ", ao2.formalname
            , ", ", ao3.shortname, " ", ao3.formalname
            , ", ", ao4.shortname, " ", ao4.formalname
            , ", ", ao5.shortname, " ", ao5.formalname
            , ", ", ao6.shortname, " ", ao6.formalname
            , ", ", ao7.shortname, " ", ao7.formalname
            ) AS fullname,
    sn7.item_weight
    FROM fias_addrobj AS ao1
        INNER JOIN fias_addrobj AS ao2 ON (ao2.parentguid=ao1.aoguid)
        INNER JOIN fias_addrobj AS ao3 ON (ao3.parentguid=ao2.aoguid)
        INNER JOIN fias_addrobj AS ao4 ON (ao4.parentguid=ao3.aoguid)
        INNER JOIN fias_addrobj AS ao5 ON (ao5.parentguid=ao4.aoguid)
        INNER JOIN fias_addrobj AS ao6 ON (ao6.parentguid=ao5.aoguid)
        INNER JOIN fias_addrobj AS ao7 ON (ao7.parentguid=ao6.aoguid)

        INNER JOIN fias_socrbase AS sn1 ON (sn1.scname = ao1.shortname AND sn1.level = ao1.aolevel)
        INNER JOIN fias_socrbase AS sn2 ON (sn2.scname = ao2.shortname AND sn2.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn3 ON (sn3.scname = ao2.shortname AND sn3.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn4 ON (sn4.scname = ao4.shortname AND sn4.level = ao4.aolevel)
        INNER JOIN fias_socrbase AS sn5 ON (sn5.scname = ao5.shortname AND sn5.level = ao5.aolevel)
        INNER JOIN fias_socrbase AS sn6 ON (sn6.scname = ao6.shortname AND sn6.level = ao6.aolevel)
        INNER JOIN fias_socrbase AS sn7 ON (sn7.scname = ao7.shortname AND sn7.level = ao7.aolevel)
    WHERE ao1.aolevel=1)

UNION

(SELECT DISTINCT (ao8.aoguid) AS aoguid,
    ao8.aolevel,
    concat(sn1.socrname
            , ", ", sn2.socrname
            , ", ", sn3.socrname
            , ", ", sn4.socrname
            , ", ", sn5.socrname
            , ", ", sn6.socrname
            , ", ", sn7.socrname
            , ", ", sn8.socrname
            ) AS scname,
    concat(ao1.shortname, " ", ao1.formalname
            , ", ", ao2.shortname, " ", ao2.formalname
            , ", ", ao3.shortname, " ", ao3.formalname
            , ", ", ao4.shortname, " ", ao4.formalname
            , ", ", ao5.shortname, " ", ao5.formalname
            , ", ", ao6.shortname, " ", ao6.formalname
            , ", ", ao7.shortname, " ", ao7.formalname
            , ", ", ao8.shortname, " ", ao8.formalname
            ) AS fullname,
    sn8.item_weight
    FROM fias_addrobj AS ao1
        INNER JOIN fias_addrobj AS ao2 ON (ao2.parentguid=ao1.aoguid)
        INNER JOIN fias_addrobj AS ao3 ON (ao3.parentguid=ao2.aoguid)
        INNER JOIN fias_addrobj AS ao4 ON (ao4.parentguid=ao3.aoguid)
        INNER JOIN fias_addrobj AS ao5 ON (ao5.parentguid=ao4.aoguid)
        INNER JOIN fias_addrobj AS ao6 ON (ao6.parentguid=ao5.aoguid)
        INNER JOIN fias_addrobj AS ao7 ON (ao7.parentguid=ao6.aoguid)
        INNER JOIN fias_addrobj AS ao8 ON (ao8.parentguid=ao7.aoguid)

        INNER JOIN fias_socrbase AS sn1 ON (sn1.scname = ao1.shortname AND sn1.level = ao1.aolevel)
        INNER JOIN fias_socrbase AS sn2 ON (sn2.scname = ao2.shortname AND sn2.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn3 ON (sn3.scname = ao2.shortname AND sn3.level = ao2.aolevel)
        INNER JOIN fias_socrbase AS sn4 ON (sn4.scname = ao4.shortname AND sn4.level = ao4.aolevel)
        INNER JOIN fias_socrbase AS sn5 ON (sn5.scname = ao5.shortname AND sn5.level = ao5.aolevel)
        INNER JOIN fias_socrbase AS sn6 ON (sn6.scname = ao6.shortname AND sn6.level = ao6.aolevel)
        INNER JOIN fias_socrbase AS sn7 ON (sn7.scname = ao7.shortname AND sn7.level = ao7.aolevel)
        INNER JOIN fias_socrbase AS sn8 ON (sn8.scname = ao8.shortname AND sn8.level = ao8.aolevel)
    WHERE ao1.aolevel=1)
;
