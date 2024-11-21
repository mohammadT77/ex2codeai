from ex2codeai import *
from langchain_ollama.llms import OllamaLLM


llm = OllamaLLM(base_url="https://4e61-34-145-10-216.ngrok-free.app", model="llama3")


_add_spec = FuncSpec("add","add two integers (a and b)") \
                    .add_example({'a':1,'b':2}, "3") \
                    .add_example({'a':3,'b':4}, "7") \
                    .add_example({'a':-1,'b':7}, "6") \

print("_add_spec PROMPT",_add_spec.prompt())
_add_str = _add_spec.invoke(llm)
print("_add_str",_add_str)

add = _add_spec.parse(_add_str)
print(add(1,2))
exit()

_MyClass_spec = ClassSpec("MyClass","a simple class having the methods add")
_MyClass_spec.add_instance_method("add","add two integers (a and b)",
            Example({'a':1,'b':2}, "3"),
            Example({'a':3,'b':4}, "7"),
            Example({'a':-1,'b':7}, "6"))
_MyClass_spec.add_class_method("sub","add two integers (a and b)", 
            Example({'a':1,'b':2}, "3"),
            Example({'a':3,'b':4}, "7"),
            Example({'a':-1,'b':7}, "6"),)
_MyClass_spec.add_static_method("mul","add two integers (a and b)", 
            Example({'a':1,'b':2}, "2"),
            Example({'a':3,'b':4}, "12"),
            Example({'a':-1,'b':7}, "-7"),)
_MyClass_spec.add_instance_method("div","to divide two integers (a and b)",   
            Example({'a':1,'b':2}, "0.5"),
            Example({'a':3,'b':4}, "0.75"),
            )
print(_MyClass_spec.prompt())
MyClassStr = _MyClass_spec.invoke(llm)
print(MyClassStr)

MyClass = _MyClass_spec.parse(MyClassStr)

print(MyClass)
myClass = MyClass()

print(myClass.add(1,2))

# f2 = fgen.generate("fibo","fibo sequence (n)",
#                    Example({'n':1}, "1"),
#                    Example({'n':2}, "1"),
#                    Example({'n':3}, "2"),
#                    Example({'n':4}, "3"),
#                    Example({'n':5}, "5"),
#                    Example({'n':6}, "8"),)




# #