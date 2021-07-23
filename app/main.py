# Run by typing python3 main.py

## **IMPORTANT:** only collaborators on the project where you run
## this can access this web server!
"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os
import time

# import stuff for our web server
from flask import Flask, request, render_template, redirect, Markup
from utils import get_base_url
from Post_Processing import generate_haiku as generate, optimize_accuracy as optimize

# import stuff for our models
from aitextgen import aitextgen
ai = aitextgen(model_folder="trained_model")

'''
Coding center code - comment out the following 4 lines of code when ready for production
'''

#port = 12340
#base_url = get_base_url(port)
output = ""

# app = Flask(__name__, static_url_path=base_url + 'static')

app = Flask(__name__)

'''
Deployment code - uncomment the following line of code when ready for production
'''

@app.route('/')
# @app.route(base_url, methods=['GET'])
def home():
    return render_template('index.html', output=None)

@app.route('/' + "<word>")
# @app.route(base_url + "<word>")
def return_haiku(word=""):
    output_list = ai.generate(prompt = word.split(" ")[0], return_as_list = True, temperature = 1.0, max_length=20)[0].replace("\n\n", "\n").split("\n")[0:3]
    output = Markup(("<br>").join(output_list))
    app.logger.debug(output)
    return render_template('index.html', output=output)

# @app.route(base_url + "/result", methods=['POST'])
# def result():
#     output = ""
#     prompt = request.form['prompt']
#     output = ai.generate(prompt = prompt.split(" ")[0], return_as_list = True, temperature = 1.0, max_length=20)[0].split("\n\n")[0]
#     haiku = optimize(output)
#     if isinstance(haiku, list): return haiku
#     if isinstance(haiku, set):
#         if haiku[0] < score: score, final_haiku = haiku[0], haiku[1]
#     haiku = "\n".join(haiku)
#     app.logger.debug(haiku)
#     return render_template('index.html', output=haiku)


if __name__ == "__main__":
    website_url = 'cocalc3.ai-camp.org'
    print(f"Try to open\n\n    https://{website_url}" + base_url + '\n\n')

    app.run(host='0.0.0.0', port=port, debug=True)
    import sys
    sys.exit(0)
