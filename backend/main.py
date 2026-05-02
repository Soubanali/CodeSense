from flask import Flask
from flask import request, jsonify
import json
from gem_api import Explain,Eli5,Optimize,Debug

 
sample_code="""
def bubble_sort(arr):
    n = len(arr)

    for i in range(n):                 
        for j in range(n - 1):        
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


arr = [5, 3, 8, 4, 2]
print(bubble_sort(arr))
"""  

app=Flask(__name__)


@app.route("/explain", methods=["POST"])
def explain_code():
    data = request.get_json()
    code = data.get("code", sample_code)

    result = Explain(code)   
    return result


@app.route("/eli5", methods=["POST"])
def eli5_code():
    data = request.get_json()
    code = data.get("code", sample_code)

    result = Eli5(code)
    return result


@app.route("/optimize", methods=["POST"])
def optimize_code():
    data = request.get_json()  
    code = data.get("code", sample_code)

    result = Optimize(code)
    return result


@app.route("/debug", methods=["GET","POST"])
def debug_code():
    data = request.get_json()
    code = data.get("code", sample_code)

    result = Debug(code)
    return "jeooooooo"







if __name__ == "__main__":
    app.run(debug=True)

