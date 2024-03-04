#net output using binary and bipolar sigmoidal function
import math
n=int(input("Enter the number of inputs : "))
x=[]
w=[]
print("Enter the Value of Inputs : ")
for i in range(0,n):
    ele=float(input())
    x.append(ele)
print("Enter the Value of Weights : ")
for i in range(0,n):
    ele=float(input())
    w.append(ele)
print(" Inputs : ",x)
print("Weights : ",w)

y=0
for i in range(0,n):
    y=y+(x[i]*w[i])

print("net input (yin) : ",y)

binary_sig=1/(1+math.exp(-y))
bipolar_sig=-1+2/(1+math.exp(-y))

print("Yout using binary sigmoidal Function : ",binary_sig)
print("Yout using bipolar sigmoidal Function : ",bipolar_sig)
