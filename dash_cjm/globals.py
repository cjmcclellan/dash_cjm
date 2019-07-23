# give some global values for dash


cjm_font = dict(family='Arial', size=14)


def default_annotation(x, y, text):
    return dict(x=x,
                y=y,
                text=text,
                showarrow=True,
                align='center',
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='#636363',
                ax=0,
                ay=-50,
                bordercolor='#c7c7c7',
                borderwidth=2,
                borderpad=4,
                bgcolor='#ff7f0e',
                opacity=0.8
                )


def below_annotation(x, y, text):
    return dict(x=x,
                y=y,
                text=text,
                showarrow=True,
                align='center',
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='#636363',
                ax=0,
                ay=50,
                bordercolor='#c7c7c7',
                borderwidth=2,
                borderpad=4,
                bgcolor='#ff7f0e',
                opacity=0.8
                )
