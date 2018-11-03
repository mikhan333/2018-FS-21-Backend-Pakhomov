import base64
import sys
from jsonrpc.proxy import ServiceProxy



if __name__ == "__main__":
    funct = sys.argv[1]

    rpc_server = ServiceProxy('http://127.0.0.1:8000/api/')
    functions = {'question_content': rpc_server.api.question_content,
                 'question_list': rpc_server.api.question_list,
                 'question_comments': rpc_server.api.question_comments,
                 'category_detail': rpc_server.api.category_detail, }

    if len(sys.argv) == 3:
        var = sys.argv[2]
        responce = functions[funct](var)
    else:
        responce = functions[funct]()

    print(responce)