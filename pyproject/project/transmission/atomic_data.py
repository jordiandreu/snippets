from string import lower
from pkg_resources import resource_string, resource_listdir, resource_filename


def GetElementData(inputelement):
    """GetElementData(inputelement [, filename])
    Gives Symbol, Z, Atomic Weight, Density and Atomic Density of inputelement

    imputelement is either Symbol of Element in string format - case insensitive
                        or Z
    Density in g/cm3
    Atomic Density in at/cm3

    """
    #filename = resource_filename('project.transmission','ScatteringFactors/AtomicData.txt')
    filename = resource_filename(__name__, 'ScatteringFactors/AtomicData.txt')

    elementfile = file(filename)
    elementdata = elementfile.readlines()
    elementfile.close()

#    elementdata = filename

    for element in elementdata[1:]:
            symbol,z,atomicweight,density,numericdensity = element.split()

            if str(inputelement).isalpha() and lower(symbol) == lower(inputelement):
                return(symbol,int(z),float(atomicweight),float(density),float(numericdensity))

            elif str(inputelement).isdigit() and float(z) == inputelement:
                return(symbol,int(z),float(atomicweight),float(density),float(numericdensity))


    return('none',-1,-1,-1,-1)


if __name__ == "__main__":
    import sys

    print GetElementData(sys.argv[1])
