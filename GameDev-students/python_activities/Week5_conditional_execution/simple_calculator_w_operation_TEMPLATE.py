#print greetings
print('Welcome to my simple calculator!')

#get user inputs
first_num = input('Please enter first integer: ')
operation = input('Please enter operation(+,-,*,/): ')
second_num = input('Please enter second integer: ')

#if sum operation
if(operation == '+'):
    #sum the two numbers
    result = int(first_num) + int(second_num)
    #output the sum to the user
    print("The sum of number is:",result)
    
#if subtract operation
elif(operation == '-'):    
    #subtract the two numbers
    result = int(first_num) - int(second_num)
    #output the difference to the user
    print("The difference of number is:",result)
    
#if multiply operation
elif(operation == '*'):    
    #multiply the two numbers
    result = int(first_num) *int(second_num)
    #output the product to the user
    print("The product of number is:",result)
    
#if divide operation
elif(operation == '/'):    
    #sum the two numbers
    result = int(first_num) /int(second_num)
    #output the quotient to the user
    print("The quotient of number is:",result)
#operation not valid
else:
    print("Please use a valid operator")


