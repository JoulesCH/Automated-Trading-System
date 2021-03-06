import dash_bootstrap_components as dbc
from dash import html

navbar = dbc.Navbar(
                        [
                            html.A(
                                dbc.Row(
                                    [
                                        html.H1('Automated Trading System', style = {'color':'#FF8400'})
                                        # dbc.Col(html.Img(id = "logo",src= link,
                                        #                 height="70px",
                                        #                 style = {'padding-right':'40px'})),
                                    ],
                                    align="center",
                                    no_gutters=True,
                                ),
                                href="/dash",
                                style = {'margin-right':30},
                            ),
                            dbc.NavbarToggler(id="navbar-toggler"),
                            dbc.Collapse(
                                        [
                                            dbc.NavItem(dbc.NavLink("π¬ Marco TeΓ³rico", href="/dash/mt", style = {'color':'#ffffff'}), style ={'list-style-type': 'none', "font-weight": "bold",'color':'#ffffff'}),
                                            dbc.NavItem(dbc.NavLink("π― Diagrama", href="/dash/d", style = {'color':'#ffffff'}), style ={'list-style-type': 'none', "font-weight": "bold",'color':'#ffffff'}),
                                            dbc.NavItem(dbc.NavLink("π¨βπ» Repositorio", href="/dash/r", style = {'color':'#ffffff'}), style ={'list-style-type': 'none', "font-weight": "bold",'color':'#ffffff'}),
                                            dbc.NavItem(dbc.NavLink("β Pruebas", href="/dash/p", style = {'color':'#ffffff'}), style ={'list-style-type': 'none', "font-weight": "bold",'color':'#ffffff'}),
                                            dbc.NavItem(dbc.NavLink("π Conclusiones", href="/dash/c", style = {'color':'#ffffff'}), style ={'list-style-type': 'none', "font-weight": "bold",'color':'#ffffff'}),
                                           
                                        ],
                                id="navbar-collapse", 
                                navbar=True,
                             ),
                             
                        ],
                        color="dark",
                        dark=True,
                        style = {'background-color':'#ffffff'},
                        #sticky = "top",
                        className = 'navB'
                    )