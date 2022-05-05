


def f(x,a,b,c):
	return ((x**2)*a) +( x*b) + c 

def fc(x1,y1,x2,y2):
	a = y1/( (((-2) * (x1**2))+ x1 + y2 - (((-2) * (x2**2)) + x2) ))
	c = y2 - (((-2) * (x2**2)) + x2)*a 
	b = (-2)*x1*a 
	return a,b,c 

a ,b ,c = fc(200,478,66,688)
y = f(66,a,b,c)
print(a,b,c,66,y)
