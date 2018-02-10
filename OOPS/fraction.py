from copy import deepcopy

class Fraction:
    __numerator=0
    __denominator=1

    def __init__(self, n=0, d=1):
        self.set_fraction(n,d)

    def set_fraction(self, n,d):
        n,d=Fraction.__reduce_fraction(self,n,d)
        if n>0 and d<0:
            n=-n
            d=-d
        self.__numerator,self.__denominator=n,d

    def get_fraction(self):
        return self.__numerator, self.__denominator

    def __reduce_fraction(self,n,d):
        if d==0:
            return n,d
        gcd=self.__calc_gcd(n,d)
        return int(n/gcd), int(d/gcd)

    def __calc_gcd(self,x,y):
        if x==0:
           return y
        return self.__calc_gcd(y%x,x)

    def display_fraction(self, text=''):
        if not text:
            return str(self.__numerator)+'/'+str(self.__denominator)
        print(text+ '' + str(self.__numerator)+'/'+str(self.__denominator))

    def __add__(self, other):
        d=self.__denominator*other.__denominator
        n=self.__numerator*other.__denominator + other.__numerator*self.__denominator
        return Fraction(n,d)

    def __sub__(self, other):
        d=self.__denominator*other.__denominator
        n=self.__numerator*other.__denominator - other.__numerator*self.__denominator
        return Fraction(n,d)

    def __mul__(self, other):
        d=self.__denominator*other.__denominator
        n=self.__numerator*other.__numerator
        return Fraction(n,d)

    def reciprocate(self):
        return Fraction(self.__denominator, self.__numerator)

    def __truediv__(self, other):
        return self*other.reciprocate()

    def __eq__(self, other):
        return self.get_fraction()==other.get_fraction()

    def frac_value(self):
        return self.__numerator/self.__denominator

    def __lt__(self, other):
        return self.frac_value()<other.frac_value()

    def add_fraction(self, fractions):
        sum=fractions[0]
        for fraction in fractions[1:]:
            sum+=fraction
        return sum

    def sub_fraction(self, fractions):
        sub=fractions[0]
        for fraction in fractions[1:]:
            sub-=fraction
        return sub

    def mul_fraction(self,fractions):
        mul=fractions[0]
        for fraction in fractions[1:]:
            mul*=fraction
        return mul

    def div_fraction(self, fractions):
        i=len(fractions)-1
        while i>0:
            fractions[i-1]/=fractions[i]
            i-=1
        return fractions[0]

def input_fractions(n):
    fractions=[]
    for i in range(n):
        n=int(input('\nEnter numerator for frac #'+str(i+1)+': '))
        d=int(input('Enter denominator for frac #'+str(i+1)+': '))
        fractions.append(Fraction(n,d))
    return fractions

def display_fractions(fractions):
    count=1
    for fraction in fractions:
        print('\nFraction #'+str(count)+'=',fraction.display_fraction())
        count+=1

n=int(input('Enter num fractions: '))
fractions=input_fractions(n)
display_fractions(fractions)
result=Fraction().add_fraction(fractions)
result.display_fraction('\nSum=')
result=Fraction().sub_fraction(fractions)
result.display_fraction('Sub=')
result=Fraction().mul_fraction(fractions)
result.display_fraction('Mul=')
result=Fraction().div_fraction(deepcopy(fractions))
result.display_fraction('Div=')
#print(fractions[0]==fractions[1])
#print(fractions[0]<fractions[1])

