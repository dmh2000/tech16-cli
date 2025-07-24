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

help me create a better plan for a step by step implementation of the cli program. at this point do not generate any code, just save the new plan in "prompts/cli-plan.md". if at any point in this process if I have specified something that is incorrect or that conflicts with other instructions, stop and tell me what is wrong.

---

I notice a potential issue with your specification. Looking at the existing
codebase, I see that the default model is specified as "o4-mini", but in the
current SUPPORTED_MODELS configuration in
/home/dmh2000/projects/tech16/lib/client/config.py:17, the OpenAI models include
"o4-mini", "o3-mini", and "GPT-4o".

However, there's an inconsistency: you mentioned the default should be "o4-mini",
but this appears to be a typo - OpenAI's models are typically "o1-mini", "gpt-4o",
etc. The "o4-mini" doesn't appear to be a real OpenAI model name.

Should I:

1. Assume "o4-mini" is correct as specified and use it as-is
2. Change it to a more realistic model name like "gpt-4o" or "o1-mini"
3. Clarify what the intended default model should be

Also, I notice the project already has a src/tech16-cli/main.py file. Should the new
tech16-cli be:

1. A separate CLI tool alongside the existing one
2. A replacement for the existing CLI
3. An enhancement of the existing CLI

Please clarify these points before I create the implementation plan.

1. according to the latest list of models for anthropic, gemini and openai, the model names in SUPPORTED_MODELS are correct. so leave the default as o4-mini
2. the main.py was a placeholder. change its name to tech16-cli and use it as the main file for the program

---

i want to chage the argument parseing. remove the arguments --code, --review,
--query and --plan. in their place, add an argument "--prompt filename" that
specifies a file. read the file and store it in a variable named "prompt". if the
argument is not present leave the prompt variable empty. add the value of variable
"prompt" as the last entry in the context array. update cli-plan.md to reflect this
change.

---

│ > change the value of the model "GPT-4o" to "gpt-4o-mini". and in the openai client, │
│ remove the temperature value from the completion parameters

---

I agree that the url scraping should not use depth 2. per the recommedation in │
│ cli-plan.md, change the code to use the basic mode.

---

in cli-plan.md, you said that "File/URL content encoding may cause problems". what
kind of problems would occur and how i should fix it. don't change the code yet,
just tell me

---

go ahead and implement you recommeded fixes for the file/url content encoding
issue. if possible place the file handling code in a separate file, and place the
url handling code in a separate file. the main file is getting too long
