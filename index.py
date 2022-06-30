import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

covid_1 = pd.read_csv('https://raw.githubusercontent.com/yasirjumani/Covid19-DataVisualization/main/full_grouped.csv')
covid5 = covid_1.groupby(['Date','Country/Region'])[['New cases', 'New deaths', 'New recovered']].max().reset_index()
covid4 = covid_1.groupby(['Country/Region','WHO Region'])[['New cases', 'New deaths', 'New recovered']].sum().reset_index()
covid4 = covid4.rename(columns={'New deaths': 'Deaths'})

availble_country = covid5['Country/Region'].unique()
available_Continent = covid4['WHO Region'].unique()

app.layout = html.Div([
    html.H1("COVID_19 Data Visualization", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_Country",
                 options=[
                     {'label': col, 'value': col} for col in availble_country
                 ],
                 multi=False,
                 value="Albania",
                 style={'width': "40%"}
                 ),
    html.Hr(),

    html.Div([
        html.Div([dcc.Graph(id='linechart')]),

        dcc.Dropdown(id='slct_Continent',
                     options=[
                         {'label': col, 'value': col} for col in available_Continent
                     ], value='Africa'),

        html.Div([dcc.Graph(id='map')]), ])

])


@app.callback(
    [Output(component_id='linechart', component_property='figure')],
    [Output(component_id='map', component_property='figure')],
    [Input(component_id='slct_Country', component_property='value')],
    [Input(component_id='slct_Continent', component_property='value')]
)
def update_graph(option_slctd, continent_slctd):
    print(option_slctd)
    print(type(option_slctd))

    dff = covid5.copy()
    dff = dff[dff["Country/Region"] == option_slctd]

    # Plotly Express
    fig = (px.line(dff, x="Date", y=["New cases", "New deaths", "New recovered"], title="The evolution of cases")
           )
    fig.update_layout(title={'y': 0.93,
                             'x': 0.43}, titlefont={'family': 'Oswald',
                                                    'color': 'rgb(12,12,131)',
                                                    'size': 25},
                      xaxis=dict(title='<b>Date</b>',
                                 color='rgb(12,12,131)',
                                 showline=True,
                                 showgrid=True,
                                 showticklabels=True,
                                 linecolor='rgb(104, 204, 104)',
                                 linewidth=2,
                                 ticks='outside',
                                 tickfont=dict(
                                     family='Arial',
                                     size=12,
                                     color='rgb(17, 37, 239)'
                                 )

                                 ),

                      yaxis=dict(title='<b>Number of cases</b>',
                                 color='rgb(12,12,131)',
                                 showline=True,
                                 showgrid=True,
                                 showticklabels=True,
                                 linecolor='rgb(104, 204, 104)',
                                 linewidth=2,
                                 ticks='outside',
                                 tickfont=dict(
                                     family='Arial',
                                     size=12,
                                     color='rgb(17, 37, 239)'
                                 )))

    dff2 = covid4.copy()
    dff2 = dff2[dff2["WHO Region"] == continent_slctd]
    fig2 = px.choropleth(dff2, locations='Country/Region', locationmode='country names', color='Deaths',
                         title="Total deaths by WHO Region")
    fig2.update_layout(title={'y': 0.93,
                              'x': 0.5}, titlefont={'family': 'Oswald',
                                                    'color': 'rgb(12,12,131)',
                                                    'size': 25})

    return (fig, fig2)


if __name__ == '__main__':
    app.run_server(debug=True)
