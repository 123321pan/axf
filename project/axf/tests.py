from django.test import TestCase

# Create your tests here.
def function(x, y, **args):
    print(x, y, args)

function(1, 2, a=1, b=2, c=3)