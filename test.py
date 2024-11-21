# test_ex2codeai.py

import os
import pytest
from .ex2codeai import FuncSpec, ClassSpec, Example
from langchain_ollama.llms import OllamaLLM

DEFAULT_OLLAMA_BASEURL = "https://4e61-34-145-10-216.ngrok-free.app"
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

# from ex2codeai import *
# from langchain_ollama.llms import OllamaLLM


# llm = OllamaLLM(base_url="https://4e61-34-145-10-216.ngrok-free.app", model="llama3")


# _add_spec = FuncSpec("add","add two integers (a and b)") \
#                     .add_example({'a':1,'b':2}, "3") \
#                     .add_example({'a':3,'b':4}, "7") \
#                     .add_example({'a':-1,'b':7}, "6") \

# print("_add_spec PROMPT",_add_spec.prompt())
# _add_str = _add_spec.invoke(llm)
# print("_add_str",_add_str)

# add = _add_spec.parse(_add_str)
# print(add(1,2))
# exit()

# _MyClass_spec = ClassSpec("MyClass","a simple class having the methods add")
# _MyClass_spec.add_instance_method("add","add two integers (a and b)",
#             Example({'a':1,'b':2}, "3"),
#             Example({'a':3,'b':4}, "7"),
#             Example({'a':-1,'b':7}, "6"))
# _MyClass_spec.add_class_method("sub","add two integers (a and b)", 
#             Example({'a':1,'b':2}, "3"),
#             Example({'a':3,'b':4}, "7"),
#             Example({'a':-1,'b':7}, "6"),)
# _MyClass_spec.add_static_method("mul","add two integers (a and b)", 
#             Example({'a':1,'b':2}, "2"),
#             Example({'a':3,'b':4}, "12"),
#             Example({'a':-1,'b':7}, "-7"),)
# _MyClass_spec.add_instance_method("div","to divide two integers (a and b)",   
#             Example({'a':1,'b':2}, "0.5"),
#             Example({'a':3,'b':4}, "0.75"),
#             )
# print(_MyClass_spec.prompt())
# MyClassStr = _MyClass_spec.invoke(llm)
# print(MyClassStr)

# MyClass = _MyClass_spec.parse(MyClassStr)

# print(MyClass)
# myClass = MyClass()

# print(myClass.add(1,2))

# # f2 = fgen.generate("fibo","fibo sequence (n)",
# #                    Example({'n':1}, "1"),
# #                    Example({'n':2}, "1"),
# #                    Example({'n':3}, "2"),
# #                    Example({'n':4}, "3"),
# #                    Example({'n':5}, "5"),
# #                    Example({'n':6}, "8"),)




# # #