

def validate_driver(f):
	"""Check driver on"""

	def check_driver(request):
		driver = None
		if cloud:
			driver = get_driver(request.environ['cal.cloud'])
		else:
			driver = get_driver()

		if driver.active:
			return f(driver=driver, request=request)
		else:
			raise Exception('Error validate_driver')

	return check_driver

def validate_resource(f):
	def check_resource(driver, request):
		if 1 == 1:
			return f(driver=driver, request=request)
		else:
			raise Exception('Error validate_resource')
	return check_resource

def get_driver(cloud=None):
	"""Get driver from Manager driver extension"""

	return object