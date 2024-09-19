from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

quotes = ["Spread love everywhere you go. Let no one ever come to you without leaving happier - Mother Teresa", "When you reach the end of your rope, tie a knot in it and hang on - Franklin D. Roosevelt", "Always remember that you are absolutely unique. Just like everyone else - Margaret Mead"]
images = ["https://cdn.britannica.com/42/155442-050-AB85E00E/Mother-Teresa.jpg", "https://www.whitehouse.gov/wp-content/uploads/2021/01/32_franklin_d_roosevelt.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/99/Margaret_Mead_%281901-1978%29.jpg"]

def home(request):
    '''
    the main page, which will display a picture of a famous or notable person of your choosing and a quote that this person said or wrote. The quote and image will be selected at random from a list of images/quote.
    '''
    string = "Hello, world!"

    return HttpResponse(string)

def quote(request):
    '''
    the same as /, to generate one quote and one image at random.
    '''
    context = {
        'quote': quotes[0],
        'image': images[0],
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    '''
    an ancillary page which will show all quotes and images.
    '''
    string = "Show all the quotes."
    return HttpResponse(string)

def about(request):
    '''
    an about page with short biographical information about the person whose quotes you are displaying, as well as a note about the creator of this web application (you).
    '''
    string = "This is the about page."
    return HttpResponse(string)
