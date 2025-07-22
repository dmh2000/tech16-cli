## Task

You are an experienced software architect and expert in python and AI development.

We will be building an python library that implements clients that can make queries to an LLM.

- The library is named 'client' and its files will be in directory lib/client

## Client Library

- The client library will implement a 'Client' interface.
- There will be three objects that implement the client interface:
  - anthropic
  - gemini
  - openai
- each implementation will have a factory function that returns an instance of the specified object. this function is not a part of the object
  - example
    - def new_anthropic() -> instance of anthropic client
    - client = new_anthropic()
- in each client implementation, there will be a single method 'query':

  - example: def client.query(model: string, context: []string) -> string
  - model : string that specifies the model to be used
  - context: an array strings that make up the context to be sent to the LLM
  - the function will use the native python API for that provider to send the query context to the LLM with the specified model and any other arguments the API requires.
  - the function will expect to get the required API key from the environment
  - the function returns the response from the LLM or an error message

- the anthropic client will use the native anthropic python API library 'anthropic'
- the gemini client will use the native gemini python API library 'google-genai'
- the openai client will use the native opean ai python API library 'openai'

help me create a better plan for the implementation of the client library. I will address the main cli program later. do not implement any code, just create a detailed plan for implementing the client library and save it in file prompts/client-plan.md

now in directory tests/client, add test functions for the anthropic, gemini and openai clients. keep the test functions as simple as possible. use the pytest framework. organize the tests and files as you see fit.
