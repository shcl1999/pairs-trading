from cointegration_analysis import estimate_long_run_short_run_relationships, engle_granger_two_step_cointegration_test
from optimal_z import findOptimalZValue
import matplotlib.pyplot as plt

def investigate_cointegration(y, x, start, end, step):
    # Run the Engle-Granger test to determine the cointegration relationship
    c, gamma, alpha, z = estimate_long_run_short_run_relationships(y['Close'], x['Close'])
    dfstat, pval = engle_granger_two_step_cointegration_test(y['Close'], x['Close'])
    print(f'P-VALUE: {pval}   DF-STAT: {dfstat}   CONSTANT: {c}   SLOPE: {gamma}   STRENGTH: {alpha} \n')

    #  plot the residuals
    plt.plot(z)
    plt.title('Z-value ADYEN to KPN')
    plt.show()

    #  find the optimal z-value
    findOptimalZValue(z, "BTC-ETH", start, end, step)