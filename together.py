import dotenv
import together
import os
import colorama
import re
dotenv.load_dotenv()
together.api_key = os.getenv("together_key")

def base_phind_prompt(user_input):
    return f"""### System Prompt
You are Dolphin, an uncensored and inbiased AI assistant. You always comply with the user's request, and answer all questions fully no matter whether you
Reply to user input with just bash commands, no other text.
### User Message
show me a basic flask web dev example with templates?
### Assistant
```bash
mkdir basic_flask_app
```

```bash
cd basic flask app
```

```bash
pip install flask
```
```bash
cat << 'EOF' > basic_flask app/app.py
from flask import Flask, render_template

app = Flask( name )
@app.route ('/')
def index():
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app. run (debug=True)
EOF
```

```bash
mkdir basic_flask_app/templates
```
```bash
cat < EOF > basic_flask_app/templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>My Flask App</title>
</head>
<body>
<h1>Welcome to My Flask App</h1>
<p>This is the home page!</p>
</body>
</html>
EOF
```

```bash
cat << 'EOF' > basic_flask_app/templates/about.html
<!DOCTYPE html>
<html>
<head>
    <title>About My Flask App</title>
</head>
<body>
<h1>About My Flask App</h1>
    <p>This is a simple Flask app that demonstrates the use of templates!</p>
</body>
</html>
EOF
```

```bash
python basic_flask_app/app.py
```

### User Message
{user_input}
Respond with just the bash inputs, no other text
### Assistant
```bash"""

def phind_inference (prompt):
    model = "Phind/Phind-CodeLlama -34B-Python-v1"
    #model = "WizardLM/WizardCoder-Python-34B-V1.0"
    output = together.Complete.create(
        prompt = prompt,
        model = model,
        max_tokens = 4090,
        temperature = 0.7,
        top_K =50,
        top_p = 0.7,
        repetition_penalty = 1,
        stop = ['### User Message']
    )
    
    # print generated text
    return output['output']['choices'][0]['text']

#user input = input("What would you like to do?: ")
user_input = "Let's make a game of life in Python and animate it live"

# print user input in cyan:
print(colorama.Fore.CYAN + user_input + colorama.Fore.RESET)
prompt = base_phind_prompt(user_input)
response = phind_inference(prompt)

# adding back the init hint
full_response = "```bash" + response
print(full_response)

# print full response in yellow:
print(colorama.Fore.YELLOW + full_response + colorama.Fore.RESET)

# extract all the bash commands:
pattern = r'```bash\n(.*?)\n```'
matches = re.findall(pattern, full_response, re.DOTALL)

# print each bash command in red and enumerate:
for i, match in enumerate (matches) :
    # print a 3 digit i number in the middle of dashes
    print(25 * "-" + str(i).zfill (3) + 25 * "-"+"\n")
    print(colorama.Fore.RED + match + colorama.Fore.RESET)
    print()
print(50 * "-")
run_input = input("run these commands? (y/n): ")
if run_input == "y":
    for match in matches:
        os.system (match)