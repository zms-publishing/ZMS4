################################################################################
# _repositoryutil.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA	02111-1307, USA.
################################################################################

# Imports.
from App.Common import package_home
import inspect
import os
import re
# Product Imports.
from Products.zms import standard

"""
Returns system conf-basepath.
"""
def get_system_conf_basepath():
	return package_home(globals())+'/conf'


"""
Get class from py-string.
"""
# ZMS5
# def get_class(py):
#	id = re.findall('class (.*?):', py)[0]
#	exec(py)
#	return eval(id)
######
# ZMS4
def get_class(py):
	if isinstance(py,bytes):
		py = py.decode('utf-8')
	id = re.findall('class (.*?):', py)[0]
	try:
		exec(py)
		return eval(id)
	except:
		return 'Error: get_class()'

"""
Read repository from base-path.
"""
def remoteFiles(self, basepath):
	standard.writeLog(self,"[remoteFiles]: basepath=%s"%basepath)
	r = {}
	if os.path.exists(basepath):
		def traverse(base, path):
			names = os.listdir(path)
			for name in names:
				filepath = os.path.join(path, name)
				if os.path.isdir(filepath):
					traverse(base,filepath)
				elif name.startswith('__') and name.endswith('__.py'):
					# Read python-representation of repository-object
					standard.writeLog(self,"[remoteFiles]: read %s"%filepath)
					f = open(filepath,"rb")
					py = standard.pystr(f.read())
					f.close()
					# Analyze python-representation of repository-object
					d = {}
					try:
							c = get_class(py)
							d = c.__dict__
					except:
							d['revision'] = standard.writeError(self,"[traverse]: can't analyze filepath=%s"%filepath)
					id = d.get('id',name)
					rd = {}
					rd['id'] = id
					rd['filename'] = filepath[len(base)+1:]
					rd['data'] = py
					rd['version'] = d.get("revision",self.getLangFmtDate(os.path.getmtime(filepath),'eng'))
					r[rd['filename']] = rd
					# Read artefacts and avoid processing of hidden files, e.g. .DS_Store on macOS 
					for file in [x for x in names if x != name and not x.startswith('.')]:
						artefact = os.path.join(path,file)
						if os.path.isfile(artefact):
								standard.writeLog(self,"[remoteFiles]: read artefact %s"%artefact)
								f = open(artefact,"rb")
								data = f.read()
								f.close()
								rd = {}
								rd['id'] = id
								rd['filename'] = artefact[len(base)+1:]
								rd['data'] = data
								rd['version'] = self.getLangFmtDate(os.path.getmtime(artefact),'eng')
								r[rd['filename']] = rd
		traverse(basepath,basepath)
	return r


"""
Read repository from base-path.
"""
def readRepository(self, basepath, deep=True):
	standard.writeLog(self,"[readRepository]: basepath=%s"%basepath)
	r = {}
	if os.path.exists(basepath):
		def traverse(base, path, level=0):
			names = os.listdir(path)
			for name in names:
				filepath = os.path.join(path, name)
				if os.path.isdir(filepath) and (deep or level == 0):
						traverse(base, filepath, level+1)
				elif name.startswith('__') and name.endswith('__.py'):
					# Read python-representation of repository-object
					standard.writeLog(self,"[readRepository]: read %s"%filepath)
					f = open(filepath, "rb")
					py = standard.pystr(f.read())
					f.close()
					# Analyze python-representation of repository-object
					d = {}
					try:
							c = get_class(py)
							d = c.__dict__
					except:
							d['revision'] = standard.writeError(self,"[readRepository]: ")
					id = d.get('id',name)
					r[id] = {}
					for k in [x for x in d if not x.startswith('__')]:
						v = d[k]
						if inspect.isclass(v):
							dd = v.__dict__
							v = []
							for kk in [x for x in dd if not x.startswith('__')]:
								vv = dd[kk]
								# Try to read artefact.
								if 'id' in vv:
									fileprefix = vv['id'].split('/')[-1]
									for file in [x for x in names if x==fileprefix or x.startswith('%s.'%fileprefix)]:
										artefact = os.path.join(path, file)
										standard.writeLog(self,"[readRepository]: read artefact %s"%artefact)
										f = open(artefact, "rb")
										data = f.read()
										f.close()
										try:
												if isinstance(data, bytes):
														data = data.decode('utf-8')
										except:
												pass
										vv['data'] = data
										break
								v.append((py.find('\t\t%s ='%kk), vv))
							v.sort()
							v = [x[1] for x in v]
						r[id][k] = v
		traverse(basepath, basepath)
	return r