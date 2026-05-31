sub1= int(input("enter subject1 marks:"))
sub2= int(input("enter subject2 marks:"))
sub3= int(input("enter subject3 marks:"))
sub4= int(input("enter subject4 marks:"))
sub5= int(input("enter subject5 marks:"))

total= sub1+sub2+sub3+sub4+sub5
percentage=total/5

print("total marks:",total)
print("percentage:",percentage)

if percentage>=70:
    print("the result is destination")

elif percentage>=60:
    print("the result is first class")

elif percentage>=40:
    print("pass only!!")

else:
    print("failed!!!")            
