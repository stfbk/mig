from datetime import datetime

import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State

separator = '--'
df = pd.read_csv("testplan.csv")
df = df.apply(lambda col: col.map(str)) # Assumption that all fields are strings. This is done for easier implementation
app = dash.Dash(__name__) # In a real scenario, it may be best to differentiate variable types categorical, ordinal and numerical.

app.layout = html.Div([
    html.H1("Smart Interactive Test Viewer"),

    html.Label("Select Columns to Display:"),
    dcc.Dropdown(
        id='display-columns',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=df.columns.tolist(),  # Default to show all columns
        multi=True
    ),

    html.Br(),

    html.Label("Select Columns to Filter By Substring:"),
    dcc.Dropdown(
        id='filter-columns',
        options=[{'label': col, 'value': col} for col in df.columns],
        value=[],  # Default to no columns selected for filtering
        multi=True
    ),

    html.Br(),

    html.Label("Enter Substrings to Filter Rows (separate with'"+separator+"', no empty substrings):"),
    dcc.Textarea(
        id='substring-input',
        value='',
        style={'width': '100%', 'height': 50},
    ),

    html.Br(),

    html.Label("Select Filtering Logic for Substrings (AND or OR):"),
    dcc.RadioItems(
        id='filter-logic',
        options=[
            {'label': 'AND', 'value': 'and'},
            {'label': 'OR', 'value': 'or'}
        ],
        value='or',
        labelStyle={'display': 'inline-block'}
    ),

    html.Br(),

    dash_table.DataTable(
        id='table',
        page_size=10,
        style_table={'overflowX': 'auto'},  # Enables horizontal scrolling
        style_cell={
            'whiteSpace': 'normal',  # Ensures text wraps
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'minWidth': '100px', 'maxWidth': '250px' # Max width so it wraps
        }
    ),
    html.Button("Save Table as a new csv testplan", id="save-button", n_clicks=0),
    dcc.Download(id="download-dataframe-csv")
])


@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    [Input('display-columns', 'value'),
     Input('filter-columns', 'value'),
     Input('substring-input', 'value'),
     Input('filter-logic', 'value')]
)
def update_table(display_cols, filter_cols, substrings, filter_logic):
    substrings = substrings.split(separator) # Get in a list all substrings to look for

    if substrings and all(sub != "" for sub in substrings) and filter_cols:  # Only apply filtering if substrings are provided (NOT EMPTY!) and there a filter_cols
        # Using a mask for row-level filtering. Made the code efficient
        mask = pd.Series(False, index=df.index)

        for i, row in df.iterrows():
            if filter_logic == 'or':
                row_mask = False
                for substring in substrings:
                    if row[filter_cols].str.contains(substring, case=False, na=False).any():
                        row_mask = True
                        break  # Stop searching once we have a match! Short-circuit
                mask[i] = row_mask

            elif filter_logic == 'and':
                row_mask = True
                for substring in substrings:
                    if not row[filter_cols].str.contains(substring, case=False, na=False).any():
                        row_mask = False
                        break  # Stop searching once one is not found! Short-circuit
                mask[i] = row_mask
        filtered_df = df[mask]
    else:
        filtered_df = df  # No valid input provided, show all rows

    return filtered_df[display_cols].to_dict('records'), [{'name': col, 'id': col} for col in display_cols]

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("save-button", "n_clicks"),
    State("table", "data"),
    prevent_initial_call=True
)
def save_to_csv(n_clicks, table_data):
    if table_data:
        filtered_df = pd.DataFrame(table_data)
        csv_string = filtered_df.to_csv(index=False, encoding='utf-8')
        return dcc.send_string(csv_string, filename=f"filtered_table_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")

if __name__ == '__main__':
    app.run_server(debug=True)