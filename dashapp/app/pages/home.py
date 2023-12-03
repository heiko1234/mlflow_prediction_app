import dash
from dash import html, dcc
from dash import callback_context


from app.utilities.cards import (
    home_card
)


dash.register_page(__name__,path="/")

# dash.register_page(
#     __name__,
#     path='/second',
#     title='Home Dashboard',
#     name='Home Dashboard'
# )


layout = html.Div(
    id="home_page_content",
    className="home_page_content",
    children=[
        html.Div(
            className="home_page_subcontent",
            children=[
                home_card(
                    id="Predictcard",
                    header_text="Predict",
                    text="Use your model to predict something",
                    icon="ai1",
                    href="predict"
                ),
                home_card(
                    id="Optimizercard",
                    header_text="Optimize",
                    text="Use your model to optimize your target",
                    icon="ai1",
                    href="optimizer"
                ),
                # home_card(
                #     id="datacard",
                #     header_text="Data",
                #     text="this is the data page",
                #     icon="data",
                #     href="dataload"
                # ),
            ],
        ),
    ],
)

