insert into fias_addrobjindex (aoguid, aolevel, scname, fullname)
(SELECT
	ao.aoguid, ao.aolevel,
	(SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao.shortname AND sn.level=ao.aolevel) as scname,
	concat(ao.shortname, " ", ao.formalname) as fullname
	FROM fias_addrobj as ao
	where ao.aolevel=1)
union
(select
	ao2.aoguid, ao2.aolevel,
	concat((SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao1.shortname AND sn.level=ao1.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao2.shortname AND sn.level=ao2.aolevel)) as scname,
	concat(ao1.shortname, " ", ao1.formalname, ", ", ao2.shortname, " ", ao2.formalname) as fullname
	from
		fias_addrobj as ao1
	inner join
		fias_addrobj as ao2
	on (ao2.parentguid=ao1.aoguid)
	where ao1.aolevel=1)
union
(select
	ao3.aoguid, ao3.aolevel,
	concat((SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao1.shortname AND sn.level=ao1.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao2.shortname AND sn.level=ao2.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao3.shortname AND sn.level=ao3.aolevel)) as scname,
	concat(ao1.shortname, " ", ao1.formalname, ", ", ao2.shortname, " ", ao2.formalname, ", ", ao3.shortname, " ", ao3.formalname) as fullname
	from
		fias_addrobj as ao1
	inner join
		fias_addrobj as ao2
	on (ao2.parentguid=ao1.aoguid)
	inner join
		fias_addrobj as ao3
	on (ao3.parentguid=ao2.aoguid)
	where ao1.aolevel=1)
union
(select
	ao4.aoguid, ao4.aolevel,
	concat((SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao1.shortname AND sn.level=ao1.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao2.shortname AND sn.level=ao2.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao3.shortname AND sn.level=ao3.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao4.shortname AND sn.level=ao4.aolevel)) as scname,
	concat(ao1.shortname, " ", ao1.formalname, ", ", ao2.shortname, " ", ao2.formalname, ", ", ao3.shortname, " ", ao3.formalname, ", ", ao4.shortname, " ", ao4.formalname) as fullname
	from
		fias_addrobj as ao1
	inner join
		fias_addrobj as ao2
	on (ao2.parentguid=ao1.aoguid)
	inner join
		fias_addrobj as ao3
	on (ao3.parentguid=ao2.aoguid)
	inner join
		fias_addrobj as ao4
	on (ao4.parentguid=ao3.aoguid)
	where ao1.aolevel=1)
union
(select
	ao5.aoguid, ao5.aolevel,
	concat((SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao1.shortname AND sn.level=ao1.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao2.shortname AND sn.level=ao2.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao3.shortname AND sn.level=ao3.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao4.shortname AND sn.level=ao4.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao5.shortname AND sn.level=ao5.aolevel)) as scname,
	concat(ao1.shortname, " ", ao1.formalname, ", ", ao2.shortname, " ", ao2.formalname, ", ", ao3.shortname, " ", ao3.formalname, ", ", ao4.shortname, " ", ao4.formalname, ", ", ao5.shortname, " ", ao5.formalname) as fullname
	from
		fias_addrobj as ao1
	inner join
		fias_addrobj as ao2
	on (ao2.parentguid=ao1.aoguid)
	inner join
		fias_addrobj as ao3
	on (ao3.parentguid=ao2.aoguid)
	inner join
		fias_addrobj as ao4
	on (ao4.parentguid=ao3.aoguid)
	inner join
		fias_addrobj as ao5
	on (ao5.parentguid=ao4.aoguid)
	where ao1.aolevel=1)
union
(select
	ao6.aoguid, ao6.aolevel,
	concat((SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao1.shortname AND sn.level=ao1.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao2.shortname AND sn.level=ao2.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao3.shortname AND sn.level=ao3.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao4.shortname AND sn.level=ao4.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao5.shortname AND sn.level=ao5.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao6.shortname AND sn.level=ao6.aolevel)) as scname,
	concat(ao1.shortname, " ", ao1.formalname, ", ", ao2.shortname, " ", ao2.formalname, ", ", ao3.shortname, " ", ao3.formalname, ", ", ao4.shortname, " ", ao4.formalname, ", ", ao5.shortname, " ", ao5.formalname, ", ", ao6.shortname, " ", ao6.formalname) as fullname
	from
		fias_addrobj as ao1
	inner join
		fias_addrobj as ao2
	on (ao2.parentguid=ao1.aoguid)
	inner join
		fias_addrobj as ao3
	on (ao3.parentguid=ao2.aoguid)
	inner join
		fias_addrobj as ao4
	on (ao4.parentguid=ao3.aoguid)
	inner join
		fias_addrobj as ao5
	on (ao5.parentguid=ao4.aoguid)
	inner join
		fias_addrobj as ao6
	on (ao6.parentguid=ao5.aoguid)
	where ao1.aolevel=1)
union
(select
	ao6.aoguid, ao6.aolevel,
	concat((SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao1.shortname AND sn.level=ao1.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao2.shortname AND sn.level=ao2.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao3.shortname AND sn.level=ao3.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao4.shortname AND sn.level=ao4.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao5.shortname AND sn.level=ao5.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao6.shortname AND sn.level=ao6.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao7.shortname AND sn.level=ao7.aolevel)) as scname,
	concat(ao1.shortname, " ", ao1.formalname, ", ", ao2.shortname, " ", ao2.formalname, ", ", ao3.shortname, " ", ao3.formalname, ", ", ao4.shortname, " ", ao4.formalname, ", ", ao5.shortname, " ", ao5.formalname, ", ", ao6.shortname, " ", ao6.formalname) as fullname
	from
		fias_addrobj as ao1
	inner join
		fias_addrobj as ao2
	on (ao2.parentguid=ao1.aoguid)
	inner join
		fias_addrobj as ao3
	on (ao3.parentguid=ao2.aoguid)
	inner join
		fias_addrobj as ao4
	on (ao4.parentguid=ao3.aoguid)
	inner join
		fias_addrobj as ao5
	on (ao5.parentguid=ao4.aoguid)
	inner join
		fias_addrobj as ao6
	on (ao6.parentguid=ao5.aoguid)
	inner join
		fias_addrobj as ao7
	on (ao7.parentguid=ao6.aoguid)
	where ao1.aolevel=1)
union
(select
	ao8.aoguid, ao8.aolevel,
	concat((SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao1.shortname AND sn.level=ao1.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao2.shortname AND sn.level=ao2.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao3.shortname AND sn.level=ao3.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao4.shortname AND sn.level=ao4.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao5.shortname AND sn.level=ao5.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao6.shortname AND sn.level=ao6.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao7.shortname AND sn.level=ao7.aolevel), ", ", (SELECT sn.socrname FROM fias_socrbase AS sn WHERE sn.scname=ao8.shortname AND sn.level=ao8.aolevel)) as scname,
	concat(ao1.shortname, " ", ao1.formalname, ", ", ao2.shortname, " ", ao2.formalname, ", ", ao3.shortname, " ", ao3.formalname, ", ", ao4.shortname, " ", ao4.formalname, ", ", ao5.shortname, " ", ao5.formalname, ", ", ao6.shortname, " ", ao6.formalname, ", ", ao7.shortname, " ", ao7.formalname, ", ", ao8.shortname, " ", ao8.formalname) as fullname
	from
		fias_addrobj as ao1
	inner join
		fias_addrobj as ao2
	on (ao2.parentguid=ao1.aoguid)
	inner join
		fias_addrobj as ao3
	on (ao3.parentguid=ao2.aoguid)
	inner join
		fias_addrobj as ao4
	on (ao4.parentguid=ao3.aoguid)
	inner join
		fias_addrobj as ao5
	on (ao5.parentguid=ao4.aoguid)
	inner join
		fias_addrobj as ao6
	on (ao6.parentguid=ao5.aoguid)
	inner join
		fias_addrobj as ao7
	on (ao7.parentguid=ao6.aoguid)
	inner join
		fias_addrobj as ao8
	on (ao8.parentguid=ao7.aoguid)
	where ao1.aolevel=1)
;