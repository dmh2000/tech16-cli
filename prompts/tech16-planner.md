create a new main program in src/tech16-planner. this cli program will be similar to src/tech16-cli, but with changes to the input arguments and functionality.

the program will have one named argument, '--model (model name)'. This argument must be the first argument after the program name. following that is any number of filenames and urls.
urls are to be scraped by beautifulsoup.
The program will have a built in system prompt, stored in a string. For now just create a placeholder for that prompt.
The system prompt and the input files and urls are combined into the context submitted to the LLM.
The output is printed on STDOUT.

If any of these requirements is not feasible or has conflicts, let me know before you generate the plan and I will fix it.

use this description to create a comprehensive implementation plan. do not create any code yet, just the plan.
