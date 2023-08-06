#!/usr/bin/env python3

# PYTHON_ARGCOMPLETE_OK

import os, sys, re, json, requests, xmltodict, shutil, base64

from copy import copy
from datetime import datetime
from io import StringIO, BytesIO
from dotmap import DotMap

from Perdy.parser import doParse, printXML
from Perdy.pretty import prettyPrint
from Argumental.Argue import Argue
from Spanners.Squirrel import Squirrel

args = Argue()
squirrel = Squirrel()

dts = '%Y-%m-%dT%H:%M:%S'


#________________________________________________________________
class Silencer(object):
	def write(self, *args, **kwargs):
		pass
	def close(self):
		pass
	def flush(self):
		pass


#________________________________________________________________
@args.command(name='step')
class STEP(object):
	'''
	base class to store the common properties and operations
	'''
	
	@args.property(short='H', default='http://host')
	def hostname(self): return

	@args.property(short='U', default='stepsys')
	def username(self): return

	@args.property(short='P')
	def password(self): return squirrel.get('stibo:%s:%s'%(self.hostname, self.username))

	@args.property(short='v', flag=True)
	def verbose(self): return

	@args.property(short='x', flag=True, help='output in xml')
	def asXML(self): return

	@args.property(short='o', help='output to a file')
	def output(self): return None

	@args.property(short='C', default='Context1')
	def context(self): return
	
	@args.property(short='W', default='Main')
	def workspace(self): return

	@args.property(short='V')
	def version(self): return

	@args.property(short='F')
	def format(self): return

	@args.property(short='X')
	def xslt(self): return

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		if asXML: self.asXML = asXML
		if verbose: self.verbose = verbose
		if output: self.output = output
		if hostname: self.hostname = hostname
		if username: self.username = username
		if context: self.context=context
		if workspace: self.workspace = workspace
		self.silent = silent
		tipe = 'application/xml' if self.asXML else 'application/json'
		self.headers={
			'Accept': tipe,
			#'Content-Type': tipe
		}
		self.path = 'restapi' if self.asXML else 'restapiv2'

		
	def process(self, path, params=None, kwargs=dict()):
		'''
		shared get operation
		'''
		url = '%s/%s/%s'%(self.hostname, self.path, path)
		auth= (self.username, self.password)
		params={
			"context" : self.context,
			"workspace" : self.workspace
		}
		if self.verbose:
			json.dump(dict(url=url, headers=self.headers, params=params), sys.stderr, indent=4)
		result = requests.get(url=url, auth=auth, headers=self.headers, params=params, **kwargs)
		if result.status_code != 200 or self.verbose:
			sys.stderr.write('%s: %s\n'%(result, result.text))
		return result

	
	def get(self, path, params=None):
		result = self.process(path, params, kwargs=dict())
		return self.export(result.text)

	
	def put(self, path, body=None, params=None, headers=None):
		url = '%s/%s/%s'%(self.hostname, self.path, path)
		auth= (self.username, self.password)
		if not params:
			params={
				"context" : self.context,
				"workspace" : self.workspace
			}
		if not headers:
			headers = copy(self.headers)
			headers['Content-Type'] = headers['Accept']
		if self.verbose:
			json.dump(dict(url=url, headers=headers, params=params), sys.stderr, indent=4)
		result = requests.put(url=url, auth=auth, headers=headers, params=params, data=body)
		if result.status_code not in [200,201] or self.verbose:
			sys.stderr.write('%s: %s\n'%(result, result.text))
		return result.text

	
	def post(self, path, body=None, params=None, headers=None):
		url = '%s/%s/%s'%(self.hostname, self.path, path)
		auth= (self.username, self.password)
		if not params:
			params={
				"context" : self.context,
				"workspace" : self.workspace
			}
		if not headers:
			headers = copy(self.headers)
			headers['Content-Type'] = headers['Accept']
		if self.verbose:
			json.dump(dict(url=url, headers=headers, params=params), sys.stderr, indent=4)
		result = requests.post(url=url, auth=auth, headers=headers, params=params, data=body)
		if result.status_code not in [200,201] or self.verbose:
			sys.stderr.write('%s: %s\n'%(result, result.text))
		return result.text


	def delete(self, path, body=None, params=None, headers=None):
		url = '%s/%s/%s'%(self.hostname, self.path, path)
		auth= (self.username, self.password)
		if not params:
			params={
				"context" : self.context,
				"workspace" : self.workspace
			}
		if not headers:
			headers = copy(self.headers)
			headers['Content-Type'] = headers['Accept']
		if self.verbose:
			json.dump(dict(url=url, headers=headers, params=params), sys.stderr, indent=4)
		result = requests.delete(url=url, auth=auth, headers=headers, params=params, data=body)
		if result.status_code != 200 or self.verbose:
			sys.stderr.write('%s: %s\n'%(result, result.text))
		return result.text

	
	def file(self, path, destination):
		params={
			"context" : self.context,
			"workspace" : self.workspace
		}
		self.headers = None
		result = self.process(path, params=params, kwargs=dict(stream=True))
		if destination:
			with open(destination, 'wb') as output:
				result.raw.decode_content = True
				shutil.copyfileobj(result.raw, output)
		return


	def export(self, result):
		if not result: return
		result = result if self.asXML else json.loads(result)

		if self.output:
			sys.stderr.write(self.output)
			dir = os.path.dirname(self.output)
			if dir and len(dir) > 0 and not os.path.isdir(dir):
				os.makedirs(os.path.dirname(self.output))
				
			_output = open(self.output,'w')

		elif self.silent:
			_output = Silencer()
		
		else:
			_output = sys.stdout
			 
		_output.write(result)

		if self.output:
			_output.close()
			
		return result
			

#________________________________________________________________
@args.command(name='assets')
class Assets(STEP):
	'''
	MIME type assets
	'''
	
	base = 'assets'
	
	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation
	def get(self, id):
		'''
		get the asset by ID
		'''
		return super().get('%s/%s'%(self.base,id))


	@args.operation
	@args.parameter(name='output', short='o', help='where to store the content, defautls to stdout')
	def content(self, id, output=None):
		'''
		downlaod the asset to a local directory
		'''
		path='%s/%s/content'%(self.base, id)
		name='/%s/%s/%s/content'%(self.path, self.base, id)
		super().file(path=path, destination=output)


	@args.operation
	def upload(self, id, file):
		pass


	@args.operation
	def update(self, id, file):
		with open(file) as input:
			body = input.read()
			headers = { 'Content-Type' : 'application/octet-stream' }
			return super().put('%s/%s/content'%(self.base, id), body=body, headers=headers)
	

#________________________________________________________________
@args.command(name='processes')
class Processes(STEP):
	'''
	background processes running on STEP
	'''
	base = 'backgroundprocesses'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation
	def list(self):
		'''
		list the background processes
		'''
		return super().get(self.base)

	
	@args.operation
	def get(self, id):
		'''
		get the process by id
		'''
		if self.asXML:
			return super().get('%s/%s'%(self.base,id))
		else:
			return super().get('background-processes/%s'%id)

		
	@args.operation(help='get error report, JSON only !')
	def report(self, id):
		'''
		get the process by id
		'''
		return super().get('background-processes/%s/execution-report'%id)

	
	@args.operation(help='get attachments, JSON only !')
	def attachments(self, id):
		'''
		get the process by id
		'''
		return super().get('background-processes/%s/attachments'%id)

	
	@args.operation(help='get attachment metadata, JSON only !')
	def attachment_metadata(self, id, attachmentId):
		'''
		get the process by id
		'''
		return super().get('background-processes/%s/attachments/%s'%(id,attachmentId))

	@args.operation(help='get attachment content, JSON only !')
	def attachment_content(self, id, attachmentId):
		'''
		get the process by id
		'''
		return super().get('background-processes/%s/attachments/%s/content'%(id,attachmentId))

	

#________________________________________________________________
@args.command(name='instances')
class Instances(STEP):
	'''
	background processes instances running on STEP
	'''
	base = 'bgpinstance'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation
	def list(self):
		'''
		return a list of instances
		'''
		return super().get(self.base)
	

	@args.operation
	def report(self, id):
		'''
		report on the process id
		'''
		return super().get('%s/%s/executionreport'%(self.base,id))


	@args.operation
	def status(self, id):
		'''
		get the states of the process id
		'''
		return super().get('%s/%s/status'%(self.base,id))


	@args.operation
	def attachment(self, id, attchmentID):
		'''
		get the atachment by attachmentID for the process id
		'''
		return super().get('%s/%s/attachment/%s'%(self.base,id,attachmentID))


#________________________________________________________________
@args.command(name='objects')
class ObjectsByKey(STEP):

	base = 'objectsbykey'
	
	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
	

	@args.operation(help='get object by keyid and key')
	@args.parameter(name='keyid', help='the ID of object type')
	@args.parameter(name='key', help='the key of the object')
	def get(self, keyid, key):
		return super().get('%s/%s/%s'%(self.base,keyid,key))


#________________________________________________________________
@args.command(name='products')
class Products(STEP):

	base = 'products'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation(help='list the products')
	@args.parameter(name='root',short='r')
	def list(self,root='ProductsRoot'):
		return super().get('%s/%s/children'%(self.base,root))


	@args.operation(help='get product by id')
	@args.parameter(name='id', help='the ID of product')
	@args.parameter(name='save', short='s', flag=True, help='save to local /restapi')
	def get(self, id, save=False):
		result = super().get('%s/%s'%(self.base, id))
		if save:
			with open('/restapi/products/%s'%id,'w') as output:
				output.write(result)
		return result

	
	@args.operation(help='create a new product')
	@args.parameter(name='name', short='n')
	@args.parameter(name='values', short='a', nargs='*', metavar='attr=value')
	def create(self, parent, objectType, name=None, values=[]):
		body=dict(
			parent=parent,
			objectType=objectType,
			name=name,
			values=dict()
		)
		for nvp in values:
			(attr,value) = tuple(nvp.split('='))
			body['values'][attr] = dict(value=dict(value=value))
		if self.verbose:
			json.dump(body, sys.stderr, indent=4)
		result = super().post('%s'%self.base, body=json.dumps(body))
		result = json.loads(result.text)
		return result

			
	@args.operation(help='delete product by id')
	@args.parameter(name='id', help='the ID of product')
	def delete(self, id):
		result = super().delete('%s/%s'%(self.base, id))
		return result


	@args.operation(help='get children of product by id')
	@args.parameter(name='id', help='the ID of product')
	def children(self, id):
		return super().get('%s/%s/children'%(self.base,id))


	@args.operation(help='get values of product by id')
	@args.parameter(name='id', help='the ID of product')
	@args.parameter(name='attributeID', help='the ID of product')
	def values(self, id, attributeID):
		return super().get('%s/%s/values/%s'%(self.base, id, attributeID))


	@args.operation(help='get references of product by id')
	@args.parameter(name='id', help='the ID of product')
	@args.parameter(name='referenceID', help='the ID of reference')
	def references(self, id, referenceID):
		return super().get('%s/%s/references/%s'%(self.base, id, referenceID))
	
	@args.operation(help='get references of product by id')
	@args.parameter(name='id', help='the ID of product')
	@args.parameter(name='referenceID', help='the ID of reference')
	@args.parameter(name='targetID', help='the ID of target')
	@args.parameter(name='values', short='m', metavar='attr=value', nargs='*', help='metadata attribute on reference')
	@args.parameter(name='asid', short='i', flag=True, help='reference valus as lov id')
	@args.parameter(name='overwrite', short='w', flag=True, help='allow overwrite')
	def reference(self, id, referenceID, targetID, values=[], asid=False, overwrite=False):
		headers={
			"accept": "application/json",
			"Content-Type": "application/json",
		}
		payload={
			"target": targetID,
			"targetType": "product",
			"values": {
			}
		}
		for nvp in values:
			_name, _value = nvp.split('=')
			payload['values'][_name] = { 
				"calculated": False,
				"contextLocal": True,
				"value": {
					"value": _value if not asid else None,
					"valueId": _value if asid else None,
					"unit": None
				}
			}
		params = {
			"context" : self.context,
			"workspace": self.workspace,
			"allow-overwrite" : overwrite
		}
		return super().put('%s/%s/references/%s/%s'%(
			self.base, id, referenceID, targetID), body=json.dumps(payload), params=params, headers=headers
		)


	@args.operation(help='set values of product by id')
	@args.parameter(name='id', help='the ID of product')
	@args.parameter(name='attributeID', help='the ID of product')
	@args.parameter(name='value', help='the ID of product')
	def update(self, id, attributeID, value):
		headers={
			"accept": "application/json",
			"Content-Type": "application/json",
		}
		payload={
			"value": {
				"value":value
			}
		}
		return super().put('%s/%s/values/%s'%(
			self.base, id, attributeID), body=json.dumps(payload), headers=headers
		)


	@args.operation(help='get tables of product by id')
	@args.parameter(name='id', help='the ID of product')
	def tables(self, id):
		return super().get('%s/%s/tables'%(self.base,id))


	@args.operation(help='search for a product')
	@args.parameter(name='expression', help='the search expression * allowed')
	def search(self, expression):
		return super().get('basicsearch/%s'%expression)


#________________________________________________________________
@args.command(name='entities')
class Entities(STEP):

	base = 'entities'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)

		
	@args.property(short='r', default='Entity hierarchy root')
	def root(self): return
	
	@args.operation(help='list of children of entity hierarchy root')
	def list(self):
		return super().get('%s/%s/children'%(self.base,self.root))


	@args.operation(help='get entity by id')
	@args.parameter(name='id', help='the ID of entity')
	def get(self, id):
		return super().get('%s/%s'%(self.base,id))


	@args.operation(help='get children of entity by id')
	@args.parameter(name='id', help='the ID of entity')
	def children(self, id):
		return super().get('%s/%s/children'%(self.base,id))


	@args.operation(help='get values of entity by id')
	@args.parameter(name='id', help='the ID of entity')
	def values(self, id):
		return super().get('%s/%s/values'%(self.base,id))


	@args.operation(help='update values of entity by id')
	@args.parameter(name='id', help='the ID of entity')
	@args.parameter(name='name', help='attribute ID')
	@args.parameter(name='value', help='attribute Value')
	def update(self, id, name, value):
		body = json.dumps(dict(value=dict(value=value)))
		headers = { 'Content-Type' : 'application/json' }
		return super().put('%s/%s/values/%s'%(self.base, id, name), body=body, headers=headers)

	
	@args.operation(help='search for entities')
	@args.parameter(name='below_id', help='the ID of entity to search within')
	@args.parameter(name='conditionType', choices=['name'], default='name', help='the type of confidition')
	@args.parameter(name='operator', choices=['eq','exists','like','neq'], default='eq', help='comparison choices')
	@args.parameter(name='queryString', help='string to search for')
	def search(self, below_id, conditionType, operator, queryString):
		body = json.dumps({
			"condition": {
				"conditionType": "and",
				"conditions": [
					{
						"conditionType": "simplebelow",
						"topNodeId": below_id,
						"topNodeType": "entity"
					},
					{
						"conditionType": conditionType,
						"operator": operator, 
						"queryString": queryString,
					}
				]
			}
		})
		headers = { 'Content-Type' : 'application/json' }
		return super().post('%s/search'%(self.base), body=body, headers=headers)
		

#________________________________________________________________
@args.command(name='classifications')
class Classifications(STEP):

	base = 'classifications'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)

		
	@args.property(short='r', default='Metcash_Root_Metcash')
	def root(self): return
	
	@args.operation(help='list of children of classification hierarchy root')
	def list(self):
		return super().get('%s/%s/children'%(self.base,self.root))


	@args.operation(help='get classification by id')
	@args.parameter(name='id', help='the ID of classification')
	def get(self, id):
		return super().get('%s/%s'%(self.base,id))


	@args.operation(help='get children of classification by id')
	@args.parameter(name='id', help='the ID of classification')
	def references(self, parent_id, reference_id):
		return super().get('%s/%s/incoming-references/%s'%(self.base, parent_id, reference_id))

	
	@args.operation(help='get children of classification by id')
	@args.parameter(name='id', help='the ID of classification')
	def assets(self, id):
		return super().get('%s/%s/assets'%(self.base, id))

	
	@args.operation(help='get children of classification by id')
	@args.parameter(name='id', help='the ID of classification')
	def children(self, id):
		return super().get('%s/%s/children'%(self.base,id))

	
	@args.operation(help='get values of classification by id')
	@args.parameter(name='id', help='the ID of classification')
	def values(self, id):
		return super().get('%s/%s/values'%(self.base,id))
	

#________________________________________________________________
@args.command(name='endpoints')
class Endpoints(STEP):

	base = 'integrationendpoints'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation(help='get a list of endpoints')
	def list(self):
		return super().get('%s'%self.base)

	
	@args.operation(help='get a list of inbound endpoints, JSON only !')
	def list_inbound(self):
		return super().get('inbound-integration-endpoints')
	

	@args.operation(help='get the status of an inbound endpoint, JSON only !')
	def status_inbound(self, id):
		return super().get('inbound-integration-endpoints/%s/status'%id)
	

	@args.operation(help='get the background processes of an inbound endpoint, JSON only !')
	def processes_inbound(self, id):
		return super().get('inbound-integration-endpoints/%s/worker-processes'%id)
	

	@args.operation(help='get a list of outbound endpoints, JSON only !')
	def list_outbound(self):
		return super().get('outbound-integration-endpoints')
	

	@args.operation(help='get the status of an outbound endpoint, JSON only !')
	def status_outbound(self, id):
		return super().get('outbound-integration-endpoints/%s/status'%id)
	

	@args.operation(help='get the background processes of an outbound endpoint, JSON only !')
	def processes_outbound(self, id):
		return super().get('outbound-integration-endpoints/%s/worker-processes'%id)
	

	@args.operation(help='get the logs')
	def log(self, id):
		return super().get('%s/%s/log'%(self.base, id))
		

	@args.operation(help='get errors')
	def errors(self, id):
		return super().get('%s/%s/errorexcerpts'%(self.base, id))
		

	@args.operation(help='get background processes')
	def processes(self, id):
		return super().get('%s/%s/backgroundprocesses'%(self.base, id))
	

	@args.operation(help='invoke an endpoint')
	def invoke(self, id):
		return super().put('%s/%s/invoke'%(self.base, id))
											   

#________________________________________________________________
def main_ep():		
	args.parse([
		'endpoints',
		'-H','https://stibo-australia-demo.scloud.stibo.com',
		'-U','DAVE',
		'-x',
		'list',	
	])
	results = args.execute()
	if results:
		print(results)
		
#________________________________________________________________
@args.command(name='imports')
class Imports(STEP):
	'''
	MIME type imports
	'''
	
	base = 'import'
	
	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation(name='import')
	@args.parameter(name='id', help='importConfigurationId')
	@args.parameter(name='process', short='p', help='process BGP description')
	def importer(self, id, file, process=None):
		'''
		returns the process BGP ID for the import process
		'''
		params = {
			"context" : self.context,
			"workspace": self.workspace,
		}
		if process:
			params['processDescription'] = process
		with open(file,'rb') as input:
			body = input.read()
			headers = { 'Content-Type' : 'application/octet-stream' }
			result = super().post('%s/%s'%(self.base, id), body=body, headers=headers, params=params)
			return result.json()
		

#________________________________________________________________
@args.command(name='exports')
class Exports(STEP):
	'''
	MIME type exports
	'''
	
	base = 'export'
	
	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation(name='export')
	@args.parameter(name='id', help='exportConfigurationId')
	@args.parameter(name='use_context', short='c', flag=True, help='useRequestContextWorkspace')
	@args.parameter(name='process', short='p', help='process BGP description', default='triggered by rest')
	@args.parameter(name='urls', short='u', nargs='*', help='STEP URLs')
	def importer(self, id, use_context=None, process=None, urls=[]):
		'''
		returns the process BGP ID for the import process
		'''
		params = {
			"context" : self.context,
			"workspace": self.workspace,
		}
		if use_context:
			params['useRequestContextWorkspace'] = json.dumps(use_context)
		body = {
			'stepUrls': urls,
			'processDescription': process,
		}
		headers = { 'Content-Type' : 'application/json' }
		result = super().post('%s/%s'%(self.base, id), body=json.dumps(body), headers=headers, params=params)
		return result.json()

#________________________________________________________________
@args.command(name='workflow')
class Workflow(STEP):

	base = 'workflows'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation(help='get a list of workflows')
	def list(self):
		return super().get('%s'%self.base)				

	@args.operation(help='get workflow by id')
	@args.parameter(name='id', help='the ID of workflow definition')
	def get(self, id):
		return super().get('%s/%s'%(self.base,id))

	@args.operation(help='instantiate a workflow instance')
	@args.parameter(name='workflow_id', help='the ID of workflow')
	@args.parameter(name='node_id', help='the node ID')
	@args.parameter(name='node_type', flag=True, oneof=['P','E','C','A','a'], help='core node type', default='P')
	@args.parameter(name='message', short='m', help='process instance message')
	def start(self, workflow_id, node_id, node_type='P', message=''):
		'''
		instantiate a workflow process instance for node
		'''
		node_types = {
			'P': 'product',
			'E': 'entity',
			'C': 'classification',
			'A' : 'asset',
			'a' : 'attribute',
		}
		
		body = json.dumps(dict(
			node=dict(
				id=node_id,
				type=node_types[node_type]
			),
			message=message
		))
		headers = { 'Content-Type' : 'application/json' }
		return super().post('%s/%s/instances'%(self.base, workflow_id), body=body, headers=headers)		
		
		
	@args.operation(help='terminate a workflow instance')
	@args.parameter(name='workflow_id', help='the ID of workflow')
	@args.parameter(name='instance_id', help='the ID of instance')
	def terminate(self, workflow_id, instance_id):
		'''
		terminate workflow process instance
		'''
		return super().delete('%s/%s/instances/%s'%(self.base, workflow_id, instance_id))		

				
#________________________________________________________________
def main_wf():		
	args.parse([
		'workflow',
		'-H','https://stibo-australia-demo.scloud.stibo.com',
		'-U','DAVE',
		'-C','GL',
		'terminate',
		'WX_Product_WF',
		'WX_1073868143',
	])
	results = args.execute()
	if results:
		print(results)
		
#________________________________________________________________
@args.command(name='tasks')
class Task(STEP):

	base = 'workflow-tasks'

	def __init__(self, asXML=None, verbose=None, output=None, silent=True, hostname=None, username=None, context=None, workspace=None):
		super().__init__(asXML=asXML, verbose=verbose, output=output, silent=silent, hostname=hostname, username=username, context=context, workspace=workspace)
		

	@args.operation(help='get a list of workflows')
	@args.parameter(name='workflow_id', help='the ID of workflow')
	@args.parameter(name='state_id', short='s', help='state id', default='')
	@args.parameter(name='node_id', help='the node ID')
	@args.parameter(name='node_type', flag=True, oneof=['P','E','C','A','a'], help='core node type', default='P')
	@args.parameter(name='message', short='m', help='process instance message')
	def search(self, workflow_id, state_id='', node_id=None, node_type='P', message=''):
		'''
		search for workflow instances
		'''
		node_types = {
			'P': 'product',
			'E': 'entity',
			'C': 'classification',
			'A' : 'asset',
			'a' : 'attribute',
		}
		
		body = json.dumps(dict(
			workflow=workflow_id,
			state=state_id,
		))
		
		headers = { 
			'Content-Type' : 'application/json',
			'Accept' : 'application/json',
		}
			
		result = super().post('%s/search'%(self.base), body=body, headers=headers)
		
		#print(result)
		
		items = json.loads(result)
		
		instances=[]
		
		for item in items:
			instance = base64.b64decode(item)		
			instances.append(json.loads(instance.decode('UTF-8')))
		
		return instances
		
	@args.operation(help='get workflow task by id')
	@args.parameter(name='id', help='the ID of workflow task')
	def get(self, id):
		return super().get('%s/%s'%(self.base,id))
		
#________________________________________________________________
def main_task():		
	args.parse([
		'tasks',
		#'-v',
		'-H','https://stibo-australia-demo.scloud.stibo.com',
		'-U','DAVE',
		'-C','GL',
		'search',
		'WX_Product_WF',
		'-s','WX_OnHold',
	])
	results = args.execute()
	if results:
		print(json.dumps(results, indent='\t'))
		
if __name__ == '__main__': main_task() 		
