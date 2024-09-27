from django.shortcuts import render

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
    return render(request, 'restaurant/order.html')

def confirmation(request):
    '''
    a confirmation page to display after the order is placed. The confirmation page will display which items were ordered, the customer information, and the expected time at which the order will be ready (a time to be determined randomly, but within 30-60 minutes of the current date/time).
    Hint: to create the readytime, use the built-in time module and it’s functions, along with the built-in random module. You will need to experiment to learn how to use these functions together.
    '''
    return render(request, 'restaurant/confirmation.html')