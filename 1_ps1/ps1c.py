## 6.100A Pset 1: Part c
## Name: Bobby Albani
## Time Spent: 30 min
## Collaborators: None

##############################################
## Get user input for initial_deposit below ##
##############################################
initial_deposit = float(input("Enter the initial deposit: "))

#########################################################################
## Initialize other variables you need (if any) for your program below ##
#########################################################################
total_cost_of_home = 800000
percent_down_payment = 0.25
amount_saved = 0
r = 0.5
total_down_payment = percent_down_payment*total_cost_of_home #percent * total to get the down payment
#prev_r = 0 #used for bisection
steps = 0

##################################################################################################
## Determine the lowest rate of return needed to get the down payment for your dream home below ##
##################################################################################################
if initial_deposit >= total_down_payment - 100:
    r = 0.0
else:
    low = 0.0
    high = 1.0
    r = (low + high)/2
    while(total_down_payment-amount_saved>100 or total_down_payment-amount_saved<-100):
        amount_saved = initial_deposit*(1+(r/12))**(36) #compound interest equation

        if total_down_payment-amount_saved > 100:
            low = r
            r = (low + high)/2
            #Done in order to find the average of the current vs previous iteration

        elif total_down_payment-amount_saved < -100:
            high = r
            r = (low + high)/2

        if low == high: #if there's a case where we can't reach within 100 of the down payment
            steps = 0
            r = None
            break
        steps += 1
    
print("Best Savings Rate: " + str(r))
print("Steps in bisection search: " + str(steps))
