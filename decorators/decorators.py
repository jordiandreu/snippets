def currency(f):
    def wrapper(*args, **kwargs):
        return '$' + str(f(*args, **kwargs))

    return wrapper

class Product():
    
    name = ""
    price = 0
    
    def __init__(self, n, p):
        self.name = n
        self.price = p
        

    @currency
    def price_with_tax(self, tax_rate_percentage):
        """Return the price with *tax_rate_percentage* applied.
        *tax_rate_percentage* is the tax rate expressed as a float, like "7.0"
        for a 7% tax rate."""
        return self.price * (1 + (tax_rate_percentage * .01))
    
myproduct = Product("potatoes",27)
x = myproduct.price_with_tax(10)

print x


def signalsElectrometer(*args):
    """Returns a dictionary with the electrometer expected output values"""

    # Real Hardware configuration
    # In1 -> 1M (range uA)
    # Out1 -> Adlink ch0

    # Dictionary of expected values
    val = 1000000
    tol = 10
    val1 = '{0}'
    tol1 = '{1}'

    expected = { 'name' : 'Electrometer',
                'e_i0_1' : [val1, tol1] }
    
    return expected

e = signalsElectrometer(1,0.1)
print repr(e['e_i0_1'])