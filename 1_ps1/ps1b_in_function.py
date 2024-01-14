def part_b(annual_salary, percent_saved, total_cost_of_home, semi_annual_raise):
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
	return months