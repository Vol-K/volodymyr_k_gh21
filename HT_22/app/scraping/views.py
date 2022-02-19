from django.shortcuts import render
from django.contrib import messages

from .forms import CategoryForm
from scraping.tasks import processing_logic


# Rendering main page, for both methods: 'GET' & 'POST'.
def index(request):

    # Get, clean and send 'POST' request to the processing.
    if request.method == "POST":
        form = CategoryForm(request.POST)

        # Checking is form valid.
        if form.is_valid():
            selected_category = request.POST.get('field')

            # Send user data ('category') to the processing script,
            # and make requests and writhe items to the 'SQLite3' database.
            processing = processing_logic.delay(selected_category)

            # Message of the end script, show where user can see final results
            # of scraping selected category.
            popup_message = (
                "Process was started, you will check the result of processing of "
                f"'{selected_category}' on the admin side.")
            messages.success(request, popup_message)

    # Generate page for the first view, 'GET' method.
    context = {
        "form": CategoryForm()
    }
    return render(request, 'scraping/index.html', context)
