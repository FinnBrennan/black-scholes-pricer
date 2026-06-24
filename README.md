# Black-Scholes Options Pricer

[Live Demo]([https://your-app-url.streamlit.app](https://black-scholes-pricer-v9jj9pjzqhuzzhvvbd9zqn.streamlit.app))

This project is for me to learn how to take financial and mathematical models and translate them into well-structured, programmatic applications. This project so far has specifically challenged me to deeply understand a real-world quantitative finance model (the Black-Scholes options pricing formula), and build an interactive tool around it. Beyond just implementing the formula correctly which is relatively simple programmatically, my focus is on presenting the data in useful, logical, and visually intuitive ways within a clean UI, allowing the user to explore how each variable affects option pricing in real time.

<img width="1464" height="822" alt="image" src="https://github.com/user-attachments/assets/3dc92711-a568-42f4-b2b4-d4bdf7592e4a" />
<img width="1470" height="820" alt="image" src="https://github.com/user-attachments/assets/06468d08-6c1d-4431-beda-10b103bd3076" />
<img width="1462" height="727" alt="image" src="https://github.com/user-attachments/assets/f6a98bcd-0464-4e47-bfc3-3e9dcbf81c1b" />



------------------------
Current Project State: 
------------------------

- Call and Put option price calculator based on user input.
- 5 Graphs for each single variable change comparison; with bound adjustability.
- Heatmaps for Call and Put pricing against Stock Price and Volatility. 
- Simple & Clean Streamlit UI with dropdown boxes for graphs.
- Sliders for bound values.
- Persistent State -> allows for live adjustment to displayed graphs according to bound changes.
- Toggle for percentage vs decimal user input.
- Unit test for pricer black-scholes calculation function.
  


------------------------
Learning So Far 
------------------------

- Black-Scholes options pricing model - formula implementation and the financial intuition 
  behind each input variable.
- Streamlit Python library for interactive web application GUIs — core components, 
  syntax, layout, state management, and styling.
- Numpy array operations and linspace for generating data ranges.
- Matplotlib/pyplot — refreshed core knowledge, new learnings in figure styling, 
  annotations, and multi-axis formatting.
- Seaborn to create heatmap visualization of data, with light Pandas usage for data structuring.
- Clean Python application structure — separation of concerns across pricer.py, 
  charts.py, heatmap.py and app.py.
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

Version 6
- Heatmaps: 
- options2d function generates a 2D numpy array of call or put prices across a stock price vs volatility grid.
- heatmap_plotting function takes the 2D array and renders an annotated seaborn heatmap.
- main_heatmap function runs both functions as a single callable for app.py.
- Call and Put heatmaps displayed side by side in the main window.
- and minor bug fixes from previous versions.
  

Version 7 (upcoming)
- GUI restructuring for better UX. Moving bound control to sidebar, Call and Put price output to main window area, Heatmaps as main focus - graphs as secondary, seperating bound controls for graphs and heatmaps.

Future Plans
- Greeks + Implied Volatility Calculator 
