# ex2codeai

**ex2codeai** is a Python library designed to streamline the process of generating Python functions and classes based on user-defined specifications and examples. It integrates with Large Language Models (LLMs) to automate the creation of code that adheres to specific behaviors and descriptions.

---

## Features

- **Function Specification**:
  - Define function names, descriptions, and behavior with examples.
  - Automatically generate Python functions that match specified logic.
  - Parse and test generated functions.

- **Class Specification**:
  - Create Python classes with instance, class, and static methods.
  - Add method definitions with detailed descriptions and examples.
  - Generate class implementations dynamically using LLMs.

- **LLM Integration**:
  - Seamless integration with `langchain` to utilize various LLMs.
  - Customizable prompts for tailored code generation.

---

## Installation

To use `ex2codeai`, ensure you have the following installed:

- Python 3.9 or later
- `langchain` (langchain==0.3.7)
- A compatible LLM (e.g., `OllamaLLM`) (langchain-ollama==0.2.0)

Install the required dependencies:
```bash
pip install langchain
pip install your-llm-wrapper  # e.g., langchain-ollama
```


---

## Usage Workflow

1. **Initialize an LLM**: Connect to your preferred LLM using supported tools and APIs. 
    ```python
    from ex2codeai import *
    from langchain_ollama.llms import OllamaLLM

    llm = OllamaLLM(base_url="https://your-ollama-instance-url", model="your-model-name")
    ```

    **Note:** You can use Google Colab for serving Ollama. See https://github.com/mohammadT77/ollama-colab

2. **Define Specifications**: Specify the desired functions or classes, including names, descriptions, and examples.
   1. **Define Functions:**
    ```python
    # Define a function specification
    _add_spec = FuncSpec("add", "add two integers (a and b)") \
        .add_example({'a': 1, 'b': 2}, "3") \
        .add_example({'a': 3, 'b': 4}, "7") \
        .add_example({'a': -1, 'b': 7}, "6")

    print("_add_spec prompt:", _add_spec.prompt())

    # Generate the function
    _add_str = _add_spec.invoke(llm)
    print("_add_str", _add_str)

    # Parse and test the function
    add = _add_spec.parse(_add_str)
    # Or:
    add = _add_spec.generate(llm)  # calls .invoke and .parse

    print(add(1, 2))  # Output: 3

    ```
   2. **Define Classes**: 
    ```python
    # Define a class specification
    _MyClass_spec = ClassSpec("MyClass", "A simple class having methods for arithmetic operations.")
    _MyClass_spec.add_instance_method("add", "add two integers (a and b)",
        Example({'a': 1, 'b': 2}, "3"),
        Example({'a': 3, 'b': 4}, "7"))
    _MyClass_spec.add_class_method("sub", "subtract b from a",
        Example({'a': 5, 'b': 2}, "3"))
    _MyClass_spec.add_static_method("mul", "multiply two integers (a and b)",
        Example({'a': 2, 'b': 3}, "6"))
    _MyClass_spec.add_instance_method("div", "divide two integers (a and b)",
        Example({'a': 4, 'b': 2}, "2.0"))

    # Generate the class
    print(_MyClass_spec.prompt())
    MyClassStr = _MyClass_spec.invoke(llm)
    print(MyClassStr)

    # Parse and test the class
    MyClass = _MyClass_spec.parse(MyClassStr)
    myClass = MyClass()
    print(myClass.add(1, 2))  # Output: 3
    ```

3. **Test the Output**: Parse and execute the generated code to validate its correctness and functionality.

---

## Components
### Classes
1. Example:
   1. Represents an example input-output pair.
   2. Converts examples to dictionary format for LLM prompts.

2. Spec:
   1. Base class for all specifications.
   2. Includes methods for invoking LLMs and parsing their outputs.

3. FuncSpec:
   1. Extends Spec for defining and generating functions.
   2. Supports adding multiple input-output examples.

4. ClassSpec:
   1. Extends Spec for defining and generating classes.
   2. Supports instance, class, and static methods with examples.

### LLM Integration
- The library uses LangChain for interacting with LLMs.
- Prompts are constructed dynamically to guide the LLM in generating Python code.

---
## Example Prompts
The library generates structured prompts for the LLM, like the following:

### Function Prompt
```
You are a Python programmer. Your task is to write a Python function that matches the following examples.
Each example consists of an input and its respective output.

Examples:
Input: (a: 1, b: 2), Output: 3
Input: (a: 3, b: 4), Output: 7
Input: (a: -1, b: 7), Output: 6

Description:
add two integers (a and b)

Write a Python function named `add` that implements this logic. Do not include any additional explanation or comments, just the code.
```

### Class Prompt:
```
You are a Python programmer. Your task is to write a simple Python class that matches the following description and has the following methods.

Description:
A simple class having methods for arithmetic operations.

Instance Methods:
Name: add, Description: add two integers (a and b), Examples:
Input: (a: 1, b: 2), Output: 3
Input: (a: 3, b: 4), Output: 7

Class Methods:
Name: sub, Description: subtract b from a, Examples:
Input: (a: 5, b: 2), Output: 3

Static Methods:
Name: mul, Description: multiply two integers (a and b), Examples:
Input: (a: 2, b: 3), Output: 6

Write a Python class named `MyClass` that implements this logic. Do not include any additional explanation or comments, just the code.

```

---

## License

This project is licensed under the Apache License.

---

## Acknowledgments

This library is built on the `langchain` framework and leverages the power of modern LLMs to deliver flexible and efficient code generation capabilities.
