#!/bin/python

import sqlite3

conn = sqlite3.connect('cache.db')
cur = conn.cursor()

print("""
<html>
<head>
<title>Fedora FTBFS list</title>
<style>
body {
	background-color:white;
	text-color:black;
}
table,td {
	width: 100%;
	border: black 1px solid;
	padding: 0.2em;
}

td {
	font-size: 0.6 em;
}

tr.odd {
	background-color: lightgrey;
}
tr.even {
	background-color: lightgreen;
}

a:link { text-decoration: none; }
a:visited { text-decoration: none; } 
a:hover { text-decoration: underline; } 
a:active { text-decoration: underline; }

</style>
</head>
<body>
<h1>List of packages which FTBFS in Fedora</h1>

<p>
This table is generated by querying all Fedora Koji instances (primary, aarch64, ppc64, s390 ones). But it differs from list of failed builds offered by Koji itself:
</p>
<ul>
	<li>packages which got failed and then got built are not listed</li>
	<li>all architectures are checked</li>
	<li>links to buildArch tasks are provided</li>
</ul>

<p><strong>NOTE: lack of entry does not mean that package is fine.</strong> Few reasons:</p>
<ul>
<li>package may never got built</li>
<li>package could be excluded by ExclusiveArch or ExcludeArch</li>
</ul>

<hr />
<a href="#f20">Fedora 20</a>
<a href="#f21">Fedora 21</a>
<a href="#f22">Fedora 22</a>
<a href="#f23">Fedora 23</a>

		""")


kojis = { 
	'aarch64':	'arm.koji.fedoraproject.org',
	'armhfp':	'koji.fedoraproject.org',
	'i386':		'koji.fedoraproject.org',
	'noarch':	'koji.fedoraproject.org',
	'ppc64le':	'ppc.koji.fedoraproject.org',
	'ppc64':	'ppc.koji.fedoraproject.org',
	's390':		's390.koji.fedoraproject.org',
	's390x':	's390.koji.fedoraproject.org',
	'x86_64':	'koji.fedoraproject.org'
	}


tag = ''
a = 0.0

cur.execute("SELECT DISTINCT package_name, tag, nvr FROM nvrs WHERE tag LIKE 'f2%' ORDER BY tag, package_name")
for package in cur.fetchall():

	if tag != package[1]:

		if tag:
			print("</table></div>")

		tag = package[1]
		print("<div id='%s'><p>%s</p>" % (tag, tag))
		print("<table>")
		print("<tr><th>Name</th><th>nvr</th>")
		print("<th>noarch</th><th>armhfp</th><th>i386</th><th>x86_64</th><th>aarch64</th><th>ppc64</th><th>ppc64le</th><th>s390</th><th>s390x</th></tr>")

	archs = {}
	for arch in cur.execute("SELECT arch, task_id FROM nvrs WHERE package_name =  ?", [package[0]]):
		archs[arch[0]] = arch[1]

	if a%2:
		print("<tr class='even'>")
	else:
		print("<tr class='odd'>")

	a = a+1

	print("<td>%s</td><td>%s</td>" % (package[0], package[2]))

	for arch in ['noarch', 'armhfp', 'i386', 'x86_64', 'aarch64', 'ppc64', 'ppc64le', 's390', 's390x']:
		print('<td>')

		if arch in archs:
			print("<a href='http://%s/koji/taskinfo?taskID=%d'>%s</a>" % (kojis[arch], archs[arch], arch))
		else:
			print('&nbsp;')

		print('</td>')

	print('</tr>')


print("</table>")
print("</body></html>")