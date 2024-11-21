import keyword
import copy
import types
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM
import dill


def save_dill(path: str, obj):
    with open(path, "wb") as f:
        dill.dump(obj, f)

def save_module(path: str, obj_str):
    assert path.endswith(".py"), "Module path must be a .py file"
    with open(path, "w") as f:
        f.write(obj_str)


class Example:
    """
    Example input and output
    """
    def __init__(self, input: dict, output):
        self.input = input
        self.output = output

    def to_dict(self):
        return {
            "input": self.input,
            "output": self.output
        }

    def __repr__(self):
        inp = ",".join([f"{k}: {v}" for k, v in self.input.items()])
        return f"Input: ({inp}), Output: {self.output}\n"


class Spec:
    """
    Base class for all specs
    """
    PROMPT = None

    def __init__(self, name: str, desc=""):
        assert name.isidentifier() and not keyword.iskeyword(name), "Name must be a valid Python identifier"
        self.name = name
        self.desc = desc

    def to_dict(self):
        return {
            "name": self.name,
            "desc": self.desc
        }
    
    def invoke(self, llm: LLM):
        """
        Invoke the LLM with the prompt
        """
        chain = self.PROMPT | llm
        str_obj = chain.invoke(self.to_dict())
        str_obj = str_obj.replace("```", "")
        return str_obj

    def generate(self, llm: LLM) -> tuple[str, any]:
        """
        Generate the function by invoking the LLM and parsing the output (str)

        Args:
            llm (LLM): LLM
        Returns:
            str, obj
        """
        str_obj = self.invoke(llm)
        return str_obj, self.parse(str_obj)

    def parse(self, str_obj: str):
        """
        Parse the output of the LLM

        Args:
            str_obj (str): Output of the LLM
        """
        str_obj = str_obj.replace("```", "")
        exec(str_obj)
        obj = eval(self.name)
        return self._wrap_generated_obj(obj, str_obj)

    def prompt(self):
        return self.PROMPT.format(**self.to_dict())
        
    def _wrap_generated_obj(self, obj, str_obj):
        obj.__name__ = self.name
        obj.__doc__ = self.desc
        return obj
    

class FuncSpec(Spec):
    TEMPLATE = """
            You are a Python programmer. Your task is to write a Python function that matches the following examples.
            Each example consists of an input and its respective output.

            Examples:
            {examples}

            Description:
            {desc}

            Write a Python function named `{name}` that implements this logic. Do not include any additional explanation or comments, just the code.
        """
    PROMPT = PromptTemplate.from_template(TEMPLATE)

    def __init__(self, name: str, desc: str, *examples: Example):
        super().__init__(name, desc)
        self.examples = list(examples)

    def add_example(self, _input: dict, output):
        """
        Add an example to the function

        Args:
            _input (dict): Input of the example
            output: Output of the example
        """
        example = Example(_input, output)
        self.examples.append(example)
        return self

    def to_dict(self):
        d = super().to_dict()
        d["examples"] = copy.deepcopy(self.examples)
        return d
    
    def __repr__(self):
        return f"Name: {self.name}, Description: {self.desc}, Examples: {self.examples}\n"
    
    def _wrap_generated_obj(self, obj, str_obj):
        obj = super()._wrap_generated_obj(obj, str_obj)
        return obj
    

class ClassSpec(Spec):
    TEMPLATE = """
            You are a Python programmer. Your task is to write a simple Python class that matches the following description and has the following methods.

            Description:
            {desc}

            Instance Methods:
            {instance_methods}

            Class Methods:
            {class_methods}

            Static Methods:
            {static_methods}


            Write a Python class named `{name}` that implements this logic. Do not include any additional explanation or comments, just the code.
        """
    PROMPT = PromptTemplate.from_template(TEMPLATE)


    def __init__(self, name, desc):
        super().__init__(name, desc)
        self.instance_methods = []
        self.class_methods = []
        self.static_methods = []

    def add_instance_method(self, name:str, desc: str, *examples: Example):
        """
        Add an instance method to the class

        Args:
            name (str): Name of the method
            desc (str): Description of the method
            examples (Example): Examples of the method
        """
        method = FuncSpec(name, desc, *examples)
        self.instance_methods.append(method)
        return self
    
    def add_class_method(self, name:str, desc: str, *examples: Example):
        """
        Add an class method to the class
        
        Args:
            name (str): Name of the method
            desc (str): Description of the method
            examples (Example): Examples of the method
        """
        method = FuncSpec(name, desc, *examples)
        self.class_methods.append(method)
        return self
    
    def add_static_method(self, name:str, desc: str, *examples: Example):
        """
        Add a static method to the class
        
        Args:
            name (str): Name of the method
            desc (str): Description of the method
            examples (Example): Examples of the method
        """
        method = FuncSpec(name, desc, *examples)
        self.static_methods.append(method)
        return self

    def to_dict(self):
        d = super().to_dict()
        d["instance_methods"] = copy.deepcopy(self.instance_methods)
        d["class_methods"] = copy.deepcopy(self.class_methods)
        d["static_methods"] = copy.deepcopy(self.static_methods)
        return d

    def __repr__(self):
        return f"Class Name: {self.name}, Description: {self.desc}\nInstance Methods:{self.instance_methods}\nClass Methods:{self.class_methods}\nStatic Methods:{self.static_methods}\n"

class ModuleSpec(Spec):
    TEMPLATE = """
            You are a Python programmer. Your task is to write a simple Python module that matches the following description, functions and classes.

            Description:
            {desc}

            Functions:
            {functions}

            Classes:
            {classes}

            Write a Python module named `{name}` that implements this logic. Make sure you are importing the necessary modules. Do not include any additional explanation or comments, just the code.
        """
    PROMPT = PromptTemplate.from_template(TEMPLATE)

    def __init__(self, name, desc):
        super().__init__(name, desc)
        self.classes = []
        self.functions = []

    def add_class(self, name:str, desc: str, *examples: Example):
        """
        Add a class to the module

        Args:
            name (str): Name of the class
            desc (str): Description of the class
            examples (Example): Examples of the class
        """
        cls = ClassSpec(name, desc, *examples)
        self.classes.append(cls)
        return cls
    
    def add_function(self, name:str, desc: str, *examples: Example):
        """
        Add a function to the module

        Args:
            name (str): Name of the function
            desc (str): Description of the function
            examples (Example): Examples of the function
        """
        f = FuncSpec(name, desc, *examples)
        self.functions.append(f)
        return f
    

    def to_dict(self):
        d = super().to_dict()
        d["functions"] = copy.deepcopy(self.functions)
        d["classes"] = copy.deepcopy(self.classes)
        return d
    
    def parse(self, str_obj: str):
        """
        Parse the output of the LLM

        Args:
            str_obj (str): Output of the LLM
        """
        str_obj = str_obj.replace("```", "")
        module = types.ModuleType(self.name)
        exec(str_obj, module.__dict__)
        module.__doc__ = self.desc
        module.__name__ = self.name

        return self._wrap_generated_obj(module, str_obj)