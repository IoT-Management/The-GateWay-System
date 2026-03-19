import importlib

def find_plugin(obj):
	stat=None
	try:
		module=importlib.import_module(f"plugins.{obj.plugin}")
		stat=module.process(obj)
		
		return {"status":stat,"msg":"plugin found"}
	except Exception as e:
		return {"status": stat ,"msg":e}

