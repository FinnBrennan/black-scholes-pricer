#pricing calculations. 
import numpy as np
from scipy.stats import norm



# Given:
# ---
# S — current stock price                                   - V= (curr_stk_prc)
# K — the fixed price you can buy/sell at (strike price).   - V= (strike_pr)
# T — time until expiry (in years)                          - V= (time_unt_exp)
# r - risk-free interest rate (think US treasury rate)-     - V= (rsk_free_ir)
# σ (sigma) - volatility of the stock (how wildly it moves) - V= (sigma_vol)

# Output:
# ---
# Call price — fair value of the right to buy at K. - V= (call_p)
# Put price — fair value of the right to sell at K. - V= (put_p)


# ( q is the dividend yield - > just going to set to 0 for this basic implmenetation
#       will update in future iteration )

# N = norm.cdf() - A normally distributed random variable, using np.scipy.stats method cdf.

#black_scholes that takes the 5 inputs as parameters.
def black_scholes(curr_stk_prc, strike_pr, time_unt_exp, 
                  rsk_free_ir, sigma_vol, q=0,):
    """black_scholes pricer that takes the 5 inputs as parameters"""




    d1= (  np.log(curr_stk_prc/strike_pr) + ((rsk_free_ir-q + 
        ((sigma_vol**2)/2)) 
        * time_unt_exp ))  / ( sigma_vol * (np.sqrt( time_unt_exp ) ) 
                               
    )



    d2 = (  np.log(curr_stk_prc/strike_pr) + (rsk_free_ir-q 
    - ((sigma_vol**2)/2))
    * time_unt_exp )  / ( sigma_vol * (np.sqrt( time_unt_exp ) ) 
                             
    )


    call_p = ( ( curr_stk_prc * (np.exp( (-q) * time_unt_exp)) * norm.cdf( d1 )) 
    -  (strike_pr * (np.exp((-rsk_free_ir)*time_unt_exp)))* norm.cdf(d2) 
    
    )

    put_p = ( ( strike_pr * (np.exp( (-rsk_free_ir) * time_unt_exp)) 
    * norm.cdf(-d2 )) 
    -  (curr_stk_prc * (np.exp((-q)*time_unt_exp)))* norm.cdf(-d1) 
    
    )

    # Returns a call price and put price in a tuple.
    return (call_p, put_p)


# Now i have call price and put price
