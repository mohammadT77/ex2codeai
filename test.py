# test_ex2codeai.py

import os
import pytest
from .ex2codeai import *
from langchain_ollama.llms import OllamaLLM

DEFAULT_OLLAMA_BASEURL = "https://0bda-34-126-185-90.ngrok-free.app/"
DEFAULT_OLLAMA_MODEL = "llama3"

# Set up parameters for the LLM
@pytest.fixture(scope="module")
def llm():
    base_url = os.getenv("OLLAMA_BASE_URL", DEFAULT_OLLAMA_BASEURL)
    model = os.getenv("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    return OllamaLLM(base_url=base_url, model=model)

def test_funcspec_generation(llm):
    # Define a function specification
    add_spec = FuncSpec("add", "add two integers (a and b)") \
        .add_example({'a': 1, 'b': 2}, "3") \
        .add_example({'a': 3, 'b': 4}, "7") \
        .add_example({'a': -1, 'b': 7}, "6")
    
    # Generate function code
    func_code = add_spec.invoke(llm)
    assert func_code is not None, "Function code should not be None"
    
    # Parse and test the function
    add_func = add_spec.parse(func_code)
    assert add_func(1, 2) == 3
    assert add_func(3, 4) == 7
    assert add_func(-1, 7) == 6

def test_classspec_generation(llm):
    # Define a class specification
    my_class_spec = ClassSpec("MyClass", "A simple class with basic arithmetic methods")
    my_class_spec.add_instance_method("add", "add two integers (a and b)",
                                      Example({'a': 1, 'b': 2}, "3"),
                                      Example({'a': 3, 'b': 4}, "7"))
    my_class_spec.add_static_method("mul", "multiply two integers (a and b)",
                                     Example({'a': 2, 'b': 3}, "6"),
                                     Example({'a': -1, 'b': 4}, "-4"))
    
    # Generate class code
    class_code = my_class_spec.invoke(llm)
    assert class_code is not None, "Class code should not be None"
    
    # Parse and test the class
    MyClass = my_class_spec.parse(class_code)
    my_instance = MyClass()
    assert my_instance.add(1, 2) == 3
    assert MyClass.mul(2, 3) == 6


def test_module_generation(llm):
    # Define a module specification
    my_module_spec = ModuleSpec("MyModule", "A simple module with basic arithmetic functions")
    my_module_spec.add_function("add", "add two integers (a and b)", 
                                Example({'a': 1, 'b': 2}, "3"),
                                Example({'a': 3, 'b': 4}, "7"))
    my_module_spec.add_class("MyClass", "A simple class with basic arithmetic methods") \
        .add_class_method("add", "add two integers (a and b)", 
                          Example({'a': 1, 'b': 2}, "3"),
                          Example({'a': 3, 'b': 4}, "7")) \
        .add_instance_method("mul", "multiply two integers (a and b)",
                             Example({'a': 2, 'b': 3}, "6"),
                             Example({'a': -1, 'b': 4}, "-4")) \
        .add_static_method("mul", "multiply two integers (a and b)",
                           Example({'a': 2, 'b': 3}, "6"),
                           Example({'a': -1, 'b': 4}, "-4")) \
        .add_instance_method("div", "divide two integers (a and b)",
                             Example({'a': 4, 'b': 2}, "2.0"))
    
    print("prompt",my_module_spec.prompt())
    # Generate module code
    module_code = my_module_spec.invoke(llm)
    assert module_code is not None, "Module code should not be None"
    print("module_code",module_code)

    # Parse and test the module
    my_module = my_module_spec.parse(module_code)
    assert my_module.add(1, 2) == 3
    my_class_instance = my_module.MyClass()
    assert my_class_instance.add(1, 2) == 3
    

    
