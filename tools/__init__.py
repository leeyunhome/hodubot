from google.genai import types
import os
import importlib
import pkgutil
import sys

def load_all_tools():
    """Dynamically loads tools from the tools directory."""
    loaded_tools = []
    tool_functions = {}
    
    # Reload the tools package to pick up new files (optional, good for dev)
    # importlib.reload(sys.modules[__name__]) 
    
    path = os.path.dirname(__file__)
    
    for _, name, _ in pkgutil.iter_modules([path]):
        if name == "__init__":
            continue
            
        module_name = f"tools.{name}"
        
        # Check if module is already loaded, if so reload it
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)
            
        # 1. Check for new structure (SCHEMA and main)
        if hasattr(module, 'SCHEMA') and hasattr(module, 'main'):
            print(f"Loaded tool: {name}")
            # FunctionDeclaration must be wrapped in a Tool object?
            # Actually, per HongLab screenshot, they might pass a list of tools.
            # But earlier debugging showed we need to wrap FunctionDeclaration in a Tool if mixed.
            # Let's assume we return a list of declarations if we want to add them to one Tool,
            # OR return a list of Tool objects. 
            # The previous main.py successfully used `types.Tool(function_declarations=[module.SCHEMA])`.
            # Let's stick to that for now to match the SDK expectation we found.
            
            loaded_tools.append(types.Tool(function_declarations=[module.SCHEMA]))
            tool_functions[module.SCHEMA.name] = module.main
        
    return loaded_tools, tool_functions
