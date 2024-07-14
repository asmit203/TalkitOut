from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import ollama

def get_completion(prompt, model):
    response = ollama.chat(model, messages=[{
        'role': 'user',
        'content': prompt,
    }])

    return response['message']['content']
# print(get_completion(prompt, "phi"))


@api_view(["POST"])
def chatbotResponse(request):
    if request.method == "POST":
        data = request.data
        # print(data)
        Resp = get_completion(data['query'], "phi3:latest")
        return Response(Resp, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
