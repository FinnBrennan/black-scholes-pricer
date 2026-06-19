from matplotlib import pyplot as plt
import numpy as np
from pricer import black_scholes

# ==========================================================
# Call and Put price vs x_variable (Stock Price, Volatility)
# ==========================================================
def options_vs_xaxis(x_datapoints,important_x,low_multi,curr_stk_prc,
                    strike_pr, time_unt_exp, 
                    rsk_free_ir, sigma_vol, call_p, put_p, mode, x_label, title):

    call_price_datapoints = []
    put_price_datapoints = []



    for x in x_datapoints:
        if mode == "stock":
            prices = black_scholes(x, strike_pr, time_unt_exp, 
                    rsk_free_ir, sigma_vol)
        elif mode == "vol":
            prices = black_scholes(curr_stk_prc, strike_pr, time_unt_exp, 
                    rsk_free_ir, x)
        elif mode == "strike":
            prices = black_scholes(curr_stk_prc, x, time_unt_exp, 
                    rsk_free_ir, sigma_vol)
        elif mode == "time":
            prices = black_scholes(curr_stk_prc, strike_pr, x, 
                    rsk_free_ir, sigma_vol)
        elif mode == "rate":
            prices = black_scholes(curr_stk_prc, strike_pr, time_unt_exp, 
                    x, sigma_vol)


            

        call_price_datapoints.append(prices[0])
        put_price_datapoints.append(prices[1])


    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

    y1 = call_price_datapoints 
    y2 = put_price_datapoints
    x = x_datapoints 

    # Main 2 call and put option price lines
    ax.plot(x, y1, label="Call price",color = "#00B32C" )
    ax.plot(x, y2, label="Put Price ",color = "#B3000C")


    # Current option price lines at current stock price. 
    ax.plot([low_multi*important_x, important_x], [call_p, call_p], color="#00B32C", linestyle="--")
    ax.plot([low_multi*important_x, important_x], [put_p, put_p], color="#B3000C", linestyle="--")
    
    # Stock price current line
    ax.plot([important_x, important_x], [0, call_p], color="black", linestyle="--")
    ax.plot([important_x, important_x], [0, put_p], color="black", linestyle="--")

    # Intersection of current 
    ax.scatter(important_x, call_p, color="#00B32C", zorder=5)
    ax.scatter(important_x, put_p, color="#B3000C", zorder=5)
    ax.scatter(important_x, 0, color="black", zorder=5)

    # Add chart elements
    ax.set_xlabel(x_label)
    ax.set_ylabel("Options Price $")
    ax.set_title(f"Call & Put price vs {title}")
    
    ax.grid(True)

    ax.set_xlim(left=x_datapoints[0])
    ax.set_ylim(bottom = 0)

    x_offset = (x_datapoints[-1] - x_datapoints[0]) * 0.05

    ax.annotate(f'Call: ${call_p:.2f}', xy=(important_x, call_p), xytext=(important_x + x_offset, call_p + 1), color='black')
    ax.annotate(f'Put: ${put_p:.2f}', xy=(important_x, put_p), xytext=(important_x + x_offset, put_p - 2), color='black')

    ax.set_xlim(x_datapoints[0], x_datapoints[-1])

    # Display the legend to differentiate lines
    ax.legend(loc='upper left')

    # Render the graph
    fig.patch.set_facecolor('#FEEBC8')
    ax.set_facecolor('#FEEBC8')
    ax.title.set_color('black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.tick_params(colors='black')

    return fig








def call_put_stock_chart(low_multi, high_multi, user_datapoints, curr_stk_prc):

    stock_price_datapoints  = np.linspace((low_multi*curr_stk_prc),(high_multi*
                            curr_stk_prc),user_datapoints)
    
    important_x = curr_stk_prc
    return (stock_price_datapoints,important_x)


def call_put_vol_chart(low_multi, high_multi, user_datapoints, sigma_vol):

    vol_price_datapoints  = np.linspace((low_multi*sigma_vol),(high_multi*
                            sigma_vol),user_datapoints)
    
    important_x = sigma_vol
    return (vol_price_datapoints,important_x)


def call_put_strike_chart(low_multi, high_multi, user_datapoints, strike_pr):

    strike_price_datapoints  = np.linspace((low_multi*strike_pr),(high_multi*
                            strike_pr),user_datapoints)
    
    important_x = strike_pr
    return (strike_price_datapoints,important_x)


def call_put_time_chart(low_multi, high_multi, user_datapoints, time_unt_exp):

    time_price_datapoints  = np.linspace((low_multi*time_unt_exp),(high_multi*
                            time_unt_exp),user_datapoints)
    
    important_x = time_unt_exp
    return (time_price_datapoints,important_x)


def call_put_rate_chart(low_multi, high_multi, user_datapoints, rsk_free_ir):

    rate_price_datapoints  = np.linspace((low_multi*rsk_free_ir),(high_multi*
                            rsk_free_ir),user_datapoints)
    
    important_x = rsk_free_ir
    return (rate_price_datapoints,important_x)


    
