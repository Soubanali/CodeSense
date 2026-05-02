from google import genai
import requests
from data_model import Feedback_Explain,Feedback_Debug,Feedback_Eli5,Feedback_Optimize
import json
from parser import parse_code
from exec import exec_code




def api_call(code,ast,exec_res,agent,mode):
    input_prompt=f"""
You are an expert python code analysis assistant.
You are given:

{{

"code":{code}

}}


{{
"Abstract_Syntax_Tree like structure":{ast}
}}


{{    
"Actual Compiler output":{exec_res}
}}



Use all available inputs together:

Code → readability and context
AST → program structure and logic flow
Compiler output → actual runtime behavior and errors

but you have to be careful,don't mention internal mechanics in your output
ast is just to help you,don't mention it ever to confuse the user.


"""
    
    Prompt={

    "Explain":f"""{input_prompt}

Now your task is to explain the code.Give a small paragraph that describes
what the code does in a normal mature way and give an overview(not much in depth but sufficient)
if there are errors,just mention them briefly.no detail explanation.
""",

    "Eli5":f"""{input_prompt}

Your task is to explain this code like i'm a five years old kid.
use analogies and intuitive language a kid can comprehend a bit.


""",


    "debug":f"""{input_prompt}

Your task is to JUST debug the code.Using my compiler output
explain every bit of error in full detail and provide solution
and suggestions to avoid these kind of errors.

""",


    "optimize":f"""{input_prompt}

Your task is to optimize the code.
first highlight the deficiencies,tell what's wrong,and why, then
Consider time and space complexity and improve code.


"""

}
    

    if(mode=="explain"):
        response = agent.models.generate_content(
        model="gemini-3-flash-preview",
        contents=Prompt["Explain"],
        config={
        "response_mime_type": "application/json",
        "response_json_schema": Feedback_Explain.model_json_schema(),
        },
    )
        
    
    if(mode=="debug"):
        response = agent.models.generate_content(
        model="gemini-3-flash-preview",
        contents=Prompt["debug"],
        config={
        "response_mime_type": "application/json",
        "response_json_schema": Feedback_Debug.model_json_schema(),
        },
    )
        

    if(mode=="optimize"):
        response = agent.models.generate_content(
        model="gemini-3-flash-preview",
        contents=Prompt["optimize"],
        config={
        "response_mime_type": "application/json",
        "response_json_schema": Feedback_Optimize.model_json_schema(),
        },
    )
        


    if(mode=="eli5"):
        response = agent.models.generate_content(
        model="gemini-3-flash-preview",
        contents=Prompt["Eli5"],
        config={
        "response_mime_type": "application/json",
        "response_json_schema": Feedback_Eli5.model_json_schema(),
        },
    )
        


    return response














def Explain(code):
   

   mode="explain"
   ast= parse_code(code)
   exec_res=exec_code(code)
   agent = client_explain

   resp=api_call(code,ast,exec_res,agent,mode)


   return resp.candidates[0].content.parts[0].text



def Debug(code):
   

   mode="debug"
   ast= parse_code(code)
   exec_res=exec_code(code)
   agent = client_debug

   resp=api_call(code,ast,exec_res,agent,mode)


   return resp.candidates[0].content.parts[0].text




def Eli5(code):
   

   mode="eli5"
   ast= parse_code(code)
   exec_res=exec_code(code)
   agent = client_eli5

   resp=api_call(code,ast,exec_res,agent,mode)


   return resp.candidates[0].content.parts[0].text




def Optimize(code):
   

   mode="optimize"
   ast= parse_code(code)
   exec_res=exec_code(code)
   agent = client_optimize

   resp=api_call(code,ast,exec_res,agent,mode)


   return resp.candidates[0].content.parts[0].text







##AI stuff
#for every mode
client_explain = genai.Client(api_key="AIzaSyBg5K4SpzCDY2CevsMlJEdsejkz1Y-nxMs")
client_eli5=genai.Client(api_key="AIzaSyBg5K4SpzCDY2CevsMlJEdsejkz1Y-nxMs")
client_debug=genai.Client(api_key="AIzaSyBg5K4SpzCDY2CevsMlJEdsejkz1Y-nxMs")
client_optimize=genai.Client(api_key="AIzaSyBg5K4SpzCDY2CevsMlJEdsejkz1Y-nxMs")





#response = client.models.generate_content(
   #model="gemini-2.5-flash",
   # contents="give me a json repsonse gannng"
#)








#models = client.models.list()

#for m in models:
   # print(m.name)


#print(response.text)



#checking if server is running

if (__name__=="__main__"):  #only when gem_api runs directly
    url = "https://generativelanguage.googleapis.com"

    try:
        r = requests.get(url, timeout=10)
        print(r.status_code)
    except Exception as e:
        print(e)