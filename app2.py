#finalcode
# from pydantic import BaseModel as PydanticBaseModel, validate_model
# from logging import ERROR, error
# from flask.typing import StatusCode
# from flask.wrappers import Response
# from flask_api import status
from pydantic import errors,validator,StrictStr,validate_model,BaseModel
from flask_pydantic import validate
from pydantic.types import StrictInt
from flask import Flask,jsonify, request,json
from pydantic import ValidationError
from pydantic.error_wrappers import error_dict
# from werkzeug.exceptions import HTTPException
# import werkzeug


app = Flask(__name__)

# @app.errorhandler
# def handleError(err):
#     print(err)
#     return err


class OrderModel(BaseModel):
    name: StrictStr
    rollno: StrictInt
    @validator('name')
    def name_check(cls, v):
        if v=='':
            raise ValueError('Name cannot be empty string')
        if v == ' ':
            raise ValueError('Name cannot be space')
        if v.replace(" ", "").isalpha() == False:
            raise ValueError('Name cannot have integers')
        if v[0].isalpha() == False:
            raise ValueError('Name cannot have space as first character') 
        return v
    

@app.route("/hi", methods=["POST"])
@validate()

def post():
    # print(user)
    Name = request.json['name']
    RollNo = request.json['rollno']
    # print(type(Name))
    # print(Name)
    try:
        user = OrderModel(name=Name,rollno=RollNo)
    except ValidationError as exc:
        # print([exc.errors])
        final_result = []
        result={}
        mylist = exc.errors()
        # print(mylist)
        for item in mylist:
            # print(item['msg'])
            error_loc = item['loc']
            err = item['type']
            err_msg = item['msg']
            result={"error_loc":error_loc, "error": err , "errorDescription": err_msg}
            final_result.append(result)
        # print(final_result)
        return jsonify(final_result)
            # return jsonify(
            # {"error_loc":error_loc, "error": err , "errorDescription": err_msg}
            # ),422
        # # print(i['msg'] for i in [exc.errors()])
        #     # print("\n")
        # for dictionary in [exc.errors()]:
        #     err = dictionary[1]['type']
        #     err_msg = dictionary[1]['msg']
        # # print(err)
        # # print(err_msg)

        # return jsonify(
        #     {"error": err , "errorDescription": err_msg}
        #     ),422

    return user
    # if ValidationError == False:
    #     print("False")
    # print("True")
    # print(body)
    # return body


    
if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="5000")