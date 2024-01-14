def part_a(annual_salary, percent_saved, total_cost_of_home):
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
	    amount_saved += amount_saved * (r/12) #return on investment
	    amount_saved += (monthly_salary * percent_saved) #amount saved from salary
	    months += 1
	
	print("Number of months: " + str(months))
	return months