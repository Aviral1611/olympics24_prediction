from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    

    # Read the CSV files
    data_2021 = pd.read_csv("Tokyo 2021 dataset v3.csv")
    data_2024 = pd.read_csv("Tokyo 2024.csv")

    # Normalize the medal counts
    data_2021['Gold Weighted'] = data_2021['Gold Medal'] * 3
    data_2021['Silver Weighted'] = data_2021['Silver Medal'] * 2
    data_2021['Bronze Weighted'] = data_2021['Bronze Medal'] * 1
    data_2021['Total Weighted'] = data_2021['Gold Weighted'] + data_2021['Silver Weighted'] + data_2021['Bronze Weighted']

    # Calculate the percentage of total weighted medals each country has
    data_2021['Percentage'] = data_2021['Total Weighted'] / data_2021['Total Weighted'].sum()

    # Calculate expected medal count for 2024 based on percentage
    total_medals_2021 = data_2021['Total'].sum()
    data_2021['Expected Total Medals 2024'] = data_2021['Percentage'] * total_medals_2021

    # Sorting based on expected total medals for 2024
    predicted_winners_2024 = data_2021[['Team/NOC', 'Expected Total Medals 2024']].sort_values(by='Expected Total Medals 2024', ascending=False)

    # Select top 10 predicted winners
    top_10_predicted_winners = predicted_winners_2024.head(10)

    return render_template('index.html', winners=top_10_predicted_winners)

if __name__ == '__main__':
    app.run()
    
