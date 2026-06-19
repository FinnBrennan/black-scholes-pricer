------------------------

Current Project State: 

------------------------

- Call and Put option price calculator based on user input.
- 5 Graphs for each single variable change comparison; with bound adjustability.
- Simple & Clean Streamlit UI with dropdown boxes for graphs.
- Sliders for bound values
- Persistent State -> allows for live adjustment to displayed graphs according to bound changes.

------------------------

Development Progress:

------------------------

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



Version 3 (Third Commit)

- Added the remaining 3 single x-variable graphs.
- Added lower and upper bound control.
- Updated styling -> put the graphs into dropdown menu so user can select only the graphs they actually want.



Version 4 (Fourth Commit) 

- Error + Bound handling & Input Validation
- Cleaned up codebase formatting (Line Length, Comments, Structure)
- Persistent State for live graph adjustments based on bound sliders
- Added Bound Sliders to allow for real time updating.


Version 5 (Upcoming) 

- Heatmap (Call & Put price across Stock Price vs Volatility grid)
