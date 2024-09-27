from django.shortcuts import redirect, render
import random
import time

daily_specials = [
    "FireCracker Roll",
    "Red Dragon Roll",
    "Lady Bug Roll"
]

prices = {
    "Dragon Roll": 12,
    "California Roll": 6,
    "Spicy Tuna Roll": 8,
    "Salmon Roll": 8,
    "drink": 2,
    "special": 15,
    "Lady Bug Roll": 15,
    "Red Dragon Roll": 15,
    "FireCracker Roll": 15
}

# Create your views here.
def main(request):
    '''
    the page with basic information about the restaurant. the main page should include the name, location, hours of operation (displayed as a list or table), and one or more photos appropriate to such a page.
    '''
    return render(request, 'restaurant/main.html')

def order(request):
    '''
    the view for the ordering page. This view will need to create a “daily special” item (choose randomly from a list), and add it to the context dictionary for the page
    display an online order form
    '''
    today_special = random.choice(daily_specials)
    context = {
        'special': today_special
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    '''
    a confirmation page to display after the order is placed. The confirmation page will display which items were ordered, the customer information, and the expected time at which the order will be ready (a time to be determined randomly, but within 30-60 minutes of the current date/time).
    Hint: to create the readytime, use the built-in time module and it’s functions, along with the built-in random module. You will need to experiment to learn how to use these functions together.
    '''
    if request.POST:
        ready_time = time.ctime(time.time() + random.randint(1800, 3600))
        total = 0
        order = []
        for key in request.POST:
            if key == 'csrfmiddlewaretoken':
                continue
            if key in prices:
                if key == "drink":
                    drink = request.POST[key]
                    order.append(drink)
                else:
                    order.append(key)
                total += prices[key]

        context = {
            'ready_time': ready_time,
            'total': total,
            'name': request.POST['name'],
            'email': request.POST['email'],
            'phone': request.POST['phone'],
            'order': order,
            'special_instructions': request.POST['special_instructions']
        }
        print(request.POST)
        return render(request, 'restaurant/confirmation.html', context)
    
    return redirect('restaurant:order')