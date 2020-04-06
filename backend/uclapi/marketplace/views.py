from django.shortcuts import render

# The id is required so that the /marketplace/:appId
# endpoint does not lead to a 404 error. It defaults
# to None as it is used for /marketplace as well.
# The id is not used on the django side, because on the 
# react side, the react router is used to decide what 
# to render on the marketplace.
def marketplace(request, id=None):
    return render(request, 'marketplace.html')
