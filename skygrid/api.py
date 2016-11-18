class Api():
	def request(self, name, data=None):
		"""
		The Virtual method that all APIs should implement

		Attributes
		__________
		name : str
			The name of the endpoint to request

		data : str, optional
			Data that can be supplied to the request, defaults to None
		"""
		raise NotImplementedError("request must be called on a concrete Api instance")

	def close(self):
		"""
		The virtual method that closes the connection, if need be
		"""
		raise NotImplementedError("close must be called on a concrete Api instance")