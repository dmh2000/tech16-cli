create a new main program in src/tech16-coder. this cli program will be similar to src/tech16-planner but instead of planning it will be used to generate code.

the program will have one named argument, '--model (model name)'. This argument must be the first argument after the program name. following that is any number of filenames and urls.
urls are to be scraped by beautifulsoup.
The program will have a built in system prompt suitable for coding, stored in a string. For now just create a placeholder for that prompt.
The system prompt and the input files and urls are combined into the context submitted to the LLM.

The output of the llm will be one of more files delimited by triple backticks, annotated with a path and filename. This program should parse the output, extract each specified file and write it to specified path and filename. However, if a file with the same path and filename already exists, write the output with a dash '-' and 3 digit random number so it does not overwrite any existing files. Its up to the developer to move, copy and/or rename files as needed.

If any of these requirements is not feasible or has conflicts, let me know before you generate the plan and I will fix it.

use this description to create a comprehensive implementation plan. do not create any code yet, just the plan. output the plan to file "tech16-coder-implementation.md"

---

in 'src/tech16-coder/tech16-coder', create a logger object using the built in python
logging module. the logger will used to write the contents of the response from the
client.query function.

---

I had to increase the limits on max output tokens for all models because the defaults the
llm built the first time were too small
