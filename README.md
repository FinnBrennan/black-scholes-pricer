Version 1 (First Commit) 
- Simple black-scholes pricer python model. Simple formula with a simple streamlit UI layer. 

- pricer.py  holds formula function.
- app.py creates as simple streamlit UI frontend -> takes inputs -> calls pricer.py
                    - function on calculate and displays call and put option prices.


  
Version 2 (Second Commit)

- Restyled streamlit UI

- charts.py holds a main create options price vs x_variable chart function
- charts.py has seperate functions for volatility x_values and stock_price x_values.
- app.py gets x_values then generates the chart using main chart function.

- streamlit config.toml for basic colour scheming.

