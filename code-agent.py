from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import json
import os
import webbrowser

load_dotenv()
client = OpenAI()

# TOOL FUNCTIONS
def run_command(cmd: str):
    if "npm run dev" in cmd:
        os.system(f"{cmd} &")  # Non-blocking
        webbrowser.open("http://localhost:5173")
        return "Development server started. Open http://localhost:5173 to view the app."
    else:
        result = os.popen(cmd).read()
        return result or "Command executed."

def write_file(params: dict):
    path = params["path"]
    content = params["content"]

    dir_path = os.path.dirname(path)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    return f"File '{path}' created successfully."

def read_file(path: str):
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return str(e)

# TOOL REGISTRY
available_tools = {
    "run_command": run_command,
    "write_file": write_file,
    "read_file": read_file
}

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a helpful AI coding agent that can generate and modify code projects based on user instructions.

Your responses must always be valid JSON objects. To confirm, every assistant reply will be a JSON object.

You operate in a loop of: plan → action → observe → output.

For every user request:
1. Analyze the programming task and requested language.
2. Plan the files needed and the code to be written.
3. Generate code in the requested language, saved to minimal files and folders.
4. If the code requires input, avoid interactive input by:
   - Using default values in code, or
   - Accepting command line arguments, or
   - Simulating input via command line piping when running.
5. Use available tools to:
   - Write code files,
   - Read files,
   - Compile/interpret and run code,
   - Capture output or errors.
6. Wait for observation after each action before proceeding.
7. Return outputs or errors clearly.

Follow this output format strictly:
{
  "step": "string",                     # One of: plan, action, observe, output
  "content": "string",                 # Explanation or output
  "function": "Only if step is action", # Tool to call
  "input": "Input to the tool"
}

Available tools:
- "write_file": Creates files with given path and content
- "read_file": Reads files by path
- "run_command": Executes terminal commands, e.g. compilers, interpreters, or executables

Rules:
- Always do one step at a time
- Never skip to output without observation
- You can write multiple files one at a time
- You can execute scripts after writing
- Be precise and minimal in file names and folder structure

For projects requiring bundlers (like Vite):
- Plan: Create a project folder.
- Action: Run `npm create vite@latest foldername -- --template react` or similar.
- Observe: Wait for installation completion.
- Then: Write/replace needed files.
- Then: Run the dev server using `npm install` and `npm run dev` inside that folder.

User: Create a C++ file that calculates factorial of a number
→
{ "step": "plan", "content": "User wants a C++ file to calculate factorial" }
{ "step": "action", "function": "write_file", "input": { "path": "factorial.cpp", "content": "#include<iostream>\\nusing namespace std;\\n\\nint factorial(int n){ return (n==0)?1:n*factorial(n-1); }\\n\\nint main(){\\n int n; cin>>n;\\n cout<<factorial(n);\\n return 0;\\n}" } }
{ "step": "observe", "output": "File 'factorial.cpp' created successfully." }
{ "step": "action", "function": "run_command", "input": "g++ factorial.cpp -o factorial && ./factorial" }
{ "step": "observe", "output": "120" }
{ "step": "output", "content": "C++ program compiled and executed successfully." }

User: Create a C++ program for linear search in an array
→
{ "step": "plan", "content": "User wants C++ code implementing linear search on a static array" }
{ "step": "action", "function": "write_file", "input": { "path": "linear_search.cpp", "content": "// C++ code with main function and linear search implementation" } }
{ "step": "observe", "output": "File 'linear_search.cpp' created successfully." }
{ "step": "action", "function": "run_command", "input": "g++ linear_search.cpp -o linear_search && ./linear_search" }
{ "step": "observe", "output": "Running program output or compilation errors" }
{ "step": "output", "content": "C++ program compiled and executed successfully." }

User: Create a JavaScript file to print the current date and time
→
{ "step": "plan", "content": "User wants a JavaScript file to print current date and time" }
{ "step": "action", "function": "write_file", "input": { "path": "date.js", "content": "console.log(new Date().toString());" } }
{ "step": "observe", "output": "File 'date.js' created successfully." }
{ "step": "action", "function": "run_command", "input": "node date.js" }
{ "step": "observe", "output": "Fri Jun 02 2025 12:34:56 GMT+0000 (UTC)" }
{ "step": "output", "content": "JavaScript program executed successfully." }

Use this pattern for all languages and tasks.
"""

# CHAT LOOP
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            response_format={"type": "json_object"},
            messages=messages
        )

        assistant_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_response})

        try:
            parsed_response = json.loads(assistant_response)
        except json.JSONDecodeError:
            print("\u26a0\ufe0f Could not parse assistant response as JSON:")
            print(assistant_response)
            break

        step = parsed_response.get("step")

        if step == "plan":
            print(f"\U0001f9e0: {parsed_response.get('content')}")
            continue

        if step == "action":
            tool_name = parsed_response.get("function")
            tool_input = parsed_response.get("input")

            print(f"\U0001f6e0️: Calling Tool: {tool_name} with input: {tool_input}")
            if tool_name in available_tools:
                output = available_tools[tool_name](tool_input)
                messages.append({"role": "user", "content": json.dumps({"step": "observe", "output": output})})
                continue
            else:
                print(f"⚠\ufe0f Unknown tool requested: {tool_name}")
                break

        if step == "output":
            print(f"\U0001f916: {parsed_response.get('content')}")
            print("✨ Ready for your next command.")
            break