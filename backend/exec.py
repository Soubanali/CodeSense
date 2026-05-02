
import io
import sys
import traceback


def exec_code(code):

    comp_res={   # result of execution on machine

    }

    errors={

    }

    # Create buffers
    output = io.StringIO()  #file obj in ram like os walay pipes
    runtime_error=io.StringIO()
    #save old streams
    old_stdout=sys.stdout
    old_stderr=sys.stderr

    try:
        sys.stdout=output  #redirection
        sys.stderr=runtime_error
        exec(code)
    except Exception as e:  #if error
            errors["error_type"]= type(e).__name__,
            errors["message"]=str(e),
            errors["trace"]= traceback.format_exc()
    
    finally:
         # restore streams
        sys.stdout = old_stdout
        sys.stderr = old_stderr

    
    errors["run_time error"]=runtime_error.getvalue()  #captured by stderr

    if(errors["run_time error"]==''):
         errors["run_time error"]="No error occured!"


    comp_res["output"]=output.getvalue()
    comp_res["error"]=errors
    
    return comp_res





# testing
code = """

a=5
b=5
print (f"{(a*b+b)} is ur ans mate")

"""


if __name__ == "__main__":  #when run direct
    print(exec_code(code)) 






