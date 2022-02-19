from dash import Dash, html, dcc, Input, Output
import altair as alt
from vega_datasets import data


# Read in global data
movies = data.movies()
df = movies[['Production_Budget', 'Running_Time_min', 
             'Major_Genre', 'IMDB_Rating', 'IMDB_Votes', 'US_Gross']].dropna(subset=['Major_Genre'])



app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

app.layout = html.Div([
    html.Iframe(
        id='scatter',
        style={'border-width':'0', 'width':'100%', 'height':'400px'}),
    dcc.Slider(id='xslider', min=0, max=10),
    dcc.Dropdown(
            id='ycol', 
            value='Running_Time_min',
            options=[{'label': i, 'value': i} for i in df.columns])
])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value'),
    Input('ycol', 'value')
)
def plot_altairs(xmax, ycol, df=df.copy()):
    chart = alt.Chart(df[df['IMDB_Rating'] < xmax]).mark_point().encode(
        x='IMDB_Rating',
        y=ycol,
        color="Major_Genre",
        tooltip=['IMDB_Rating:N']).interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)