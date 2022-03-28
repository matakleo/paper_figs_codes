import numpy as np
import matplotlib.pyplot as plt

a=np.array([[26.221850683305096], [108.43876287248005], [96.56245245411536], [65.95236479790769], [25.09483055317783]])
print('mean = ',np.mean(a),',80th percentile = ', np.percentile(a,80),',20th percentile = ', np.percentile(a,20))
upper_error= [np.percentile(a,80)]
lower_error =  [np.percentile(a,20)]
total_error=[lower_error,upper_error]
print(total_error)
plt.bar([0],np.mean(a),yerr=total_error)
# plt.show()



# Define Data

# x = np.arange(2, 16, 1.5)
# y = np.exp(x*2)

# # Define errors

# error = 0.1 * x
# print(error)

# # Lower limit of error

# lower_error = 0.6 * error
# print(lower_error)

# # Upper limit of error

# upper_error = error
# print(upper_error)


# # plot error bars

# asymmetric_error = [lower_error, upper_error]
# print(asymmetric_error)
# plt.errorbar(x, y, xerr=asymmetric_error, fmt='o')

# Display Graph

plt.show()