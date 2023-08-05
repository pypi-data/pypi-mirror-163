from dash_labs.plugins import register_page
from dash import dcc, html, Input, Output, callback
import plotly.express as px

register_page(__name__, path="/")

df = px.data.medals_wide(indexed=True)

layout = html.Div(
    [
        html.P("Medals included:"),
        dcc.Checklist(
            id="heatmaps-medals",
            options=[{"label": x, "value": x} for x in df.columns],
            value=df.columns.tolist(),
        ),
        dcc.Graph(id="heatmaps-graph"),
    ]
)


@callback(Output("heatmaps-graph", "figure"), Input("heatmaps-medals", "value"))
def filter_heatmap(cols):
    fig = px.imshow(df[cols])
    return fig
