import keyword
import copy
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM


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
        return chain.invoke(self.to_dict())

    def generate(self, llm: LLM):
        """
        Generate the function by invoking the LLM and parsing the output (str)
        """
        return self.parse(self.invoke(llm))

    def parse(self, str_obj: str):
        """
        Parse the output of the LLM

        Args:
            str_obj (str): Output of the LLM
        """
        str_obj = str_obj.replace("```", "")
        exec(str_obj)
        return eval(self.name)

    def prompt(self):
        return self.PROMPT.format(**self.to_dict())
    

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