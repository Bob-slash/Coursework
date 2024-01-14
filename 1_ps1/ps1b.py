## 6.100A Pset 1: Part b
## Name:Bobby Albani
## Time Spent: 15 min
## Collaborators: None

##################################################################################################
## Get user input for annual_salary, percent_saved, total_cost_of_home, semi_annual_raise below ##
##################################################################################################
annual_salary = float(input("Enter your annual salary: "))
percent_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
total_cost_of_home = int(input("Enter the cost of your dream home: "))
semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

#########################################################################
## Initialize other variables you need (if any) for your program below ##
#########################################################################
percent_down_payment = 0.25
amount_saved = 0
r = 0.05
total_down_payment = percent_down_payment*total_cost_of_home #percent * total to get the down payment
monthly_salary = annual_salary/12
months = 0

###############################################################################################
## Determine how many months it would take to get the down payment for your dream home below ## 
###############################################################################################
while amount_saved < total_down_payment:
    if months % 6 == 0 and months > 0: #to apply the semi annual raise every 6 months and not the 0th month
        annual_salary += annual_salary * semi_annual_raise
        monthly_salary = annual_salary/12
    amount_saved += amount_saved * (r/12)
    amount_saved += (monthly_salary * percent_saved)
    months += 1

print("Number of months: " + str(months))
