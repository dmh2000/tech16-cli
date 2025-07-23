## Task

You are an experienced software developer and expert in python and AI development.

We will be building a cli tool, written in python, that will allow a user to make a query to an LLM and get the response.

- the main program name is tech16-cli
- on startup the program will do the following:
  - read input from stdin if there is any. if not continue
  - accept the following command line arguments in this order
    - one of the following command names (mutually exclusive) --query, --code, --plan, --review. if none is specified, default to --query
    - "--model [model name]" where the model name can be any of the supported models. if the --model argument is not specified the model will default to o4-mini
  - following the arguments, accept any number of filenames and urls. internally assign these to an array of strings
- the program will select one of 4 hard coded system prompt strings based on the first argument. the strings will have the variable names "system_query", "system_code", "system_plan", "system_review". for now, put these four strings in a separate file and have them return the variable name. later I will add the content of the strings.
- the program will create an instance of a Client of the provider type that matches the specified model
- the program will compile a 'context' array of strings based on the filenames and urls in the command line, beginning with the select system string, then:
  - if a filename is found, read its data and add it to the context array
  - if a url is found, use Requests and BeautifulSoup to scrape the url to a depth of 2 and add the results as a string to the context
- when all commands and file names have been processed and added to the context, the program will call the 'query' function of the select client and print the results on stdout.
- at any point if an error is encountered, such as invalid model, invalid command name, file not found or url not found, the program will call a function that prints an error message and exits the program.

help me create a better plan for a step by step implementation of the cli program. at this point do not generate any code, just save the new plan in "prompts/cli-plan.md"
