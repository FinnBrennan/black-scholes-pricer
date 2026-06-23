# Black-Scholes Options Pricer


------------------------
Current Project State: 
------------------------

- Call and Put option price calculator based on user input.
- 5 Graphs for each single variable change comparison; with bound adjustability.
- Simple & Clean Streamlit UI with dropdown boxes for graphs.
- Sliders for bound values.
- Persistent State -> allows for live adjustment to displayed graphs according to bound changes.
- Toggle for percentage vs decimal user input.
- Unit test for pricer black-scholes calculation function.


------------------------
Learning So Far
------------------------
- Black-Scholes options pricing model - formula implementation and financial intuition 
  behind each input variable.
- Streamlit Python library for interactive web application GUIs — core components, 
  syntax, layout, state management, and styling.
- Numpy array operations and linspace for generating data ranges.
- Matplotlib/pyplot — refreshed core knowledge, new learnings in figure styling, 
  annotations, and multi-axis formatting.
- Clean Python application structure — separation of concerns across pricer.py, 
  charts.py, and app.py.
- Python unit testing with pytest and unittest.

------------------------
Development Progress:
------------------------

Version 1 
- Simple black-scholes pricer python model. Simple formula with a simple streamlit UI layer. 
- pricer.py  holds formula function.
- app.py creates as simple streamlit UI frontend -> takes inputs -> calls pricer.py
function on calculate and displays call and put option prices.
  
Version 2 
- Restyled streamlit UI
- charts.py holds a main create options price vs x_variable chart function
- charts.py has seperate functions for volatility x_values and stock_price x_values.
- app.py gets x_values then generates the chart using main chart function.
- streamlit config.toml for basic colour scheming.



Version 3 
- Added the remaining 3 single x-variable graphs.
- Added lower and upper bound control.
- Updated styling -> put the graphs into dropdown menu so user can select only the graphs they actually want.


Version 4 
- Error + Bound handling & Input Validation
- Cleaned up codebase formatting (Line Length, Comments, Structure)
- Persistent State for live graph adjustments based on bound sliders
- Added Bound Sliders to allow for real time updating.

Version 5 
- Toggle for percentage vs decimal user input.
- Refactored chart functions for x datapoints array into 1 function. (Did not previously notice redundant code)
- Unit test for pricer -> black_scholes(). The main formula function.

Version 6 (Upcoming) 
- Heatmap (Call & Put price across Stock Price vs Volatility grid)
