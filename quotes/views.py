from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.

quotes = ["Spread love everywhere you go. Let no one ever come to you without leaving happier - Mother Teresa", "When you reach the end of your rope, tie a knot in it and hang on - Franklin D. Roosevelt", "Always remember that you are absolutely unique. Just like everyone else - Margaret Mead"]
images = ["https://cdn.britannica.com/42/155442-050-AB85E00E/Mother-Teresa.jpg", "https://www.whitehouse.gov/wp-content/uploads/2021/01/32_franklin_d_roosevelt.jpg", "https://upload.wikimedia.org/wikipedia/commons/9/99/Margaret_Mead_%281901-1978%29.jpg"]

about_desc = [
    "Mother Teresa, known in the Catholic Church as Saint Teresa of Calcutta, was an Albanian-Indian Roman Catholic nun and missionary. She was born in Skopje, then part of the Kosovo Vilayet of the Ottoman Empire. After living in Skopje for eighteen years, she moved to Ireland and then to India, where she lived for most of her life.",
    "Franklin Delano Roosevelt, commonly known by his initials FDR, was an American politician who served as the 32nd president of the United States from 1933 until his death in 1945. The longest serving U.S. president, he is the only president to have served more than two terms.",
    "Margaret Mead was an American cultural anthropologist who featured frequently as an author and speaker in the mass media during the 1960s and 1970s. She earned her bachelor's degree at Barnard College in New York City and her M.A. and Ph.D. degrees from Columbia University."
]

names = ["Mother Teresa", "Franklin D. Roosevelt", "Margaret Mead"]

def home(request):
    '''
    the main page, which will display a picture of a famous or notable person of your choosing and a quote that this person said or wrote. The quote and image will be selected at random from a list of images/quote.
    '''
    q = random.randint(0, len(quotes)-1)
    context = {
        'quote': quotes[q],
        'image': images[q],
    }
    return render(request, 'quotes/quote.html', context)

# def quote(request):
#     '''
#     the same as /, to generate one quote and one image at random.
#     '''
#     q = random.choice(quotes)
#     i = random.choice(images)
#     context = {
#         'quote': q,
#         'image': i,
#     }
#     return render(request, 'quotes/quote.html', context)

def show_all(request):
    '''
    an ancillary page which will show all quotes and images.
    '''

    context = {
        'quotes_images': zip(quotes, images),
    }
    return render(request, 'quotes/show_all.html', context)    

def about(request):
    '''
    an about page with short biographical information about the person whose quotes you are displaying, as well as a note about the creator of this web application (you).
    '''
    context = {
        'about_info': zip(names, about_desc, images),
    }

    return render(request, 'quotes/about.html', context)
