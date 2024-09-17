## hw/views.py
# description: the logic to handle URL requests
from django.shortcuts import render
from django.http import HttpResponse
import time
import random
# Create your views here.

# def home(request):
#     '''
#     A function to respond to the /hw URL.
#     '''

#     #create some text:
#     response_text = f'''
#     <html>
#         <h1>
#             Hello, world!
#         </h1>
#         <p>
#             This is the home page for the hw app.
#         </p>
#         <hr>
#         This page was generated at {time.ctime()}
#     </html>
#     '''

#     #return a response to the client
#     return HttpResponse(response_text)

def home(request):
    '''
    A function to respond to the /hw URL.
    This function will delegate work to an HTML template.
    '''

    template_name = 'hw/home.html'
    # create a context dictionary to pass variables to the template:
    context = {
        'current_time': time.ctime(),
        'letter1': chr(random.randint(65, 90)),
        'letter2': chr(random.randint(65, 90)),
        'number': random.randint(1, 10),
    }

    # delegate response to html template:
    return render(request, template_name, context)