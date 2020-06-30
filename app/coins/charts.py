import pandas as pd
from bokeh.embed import components
from bokeh.models import ColumnDataSource, FactorRange, NumeralTickFormatter, LinearAxis, DatetimeTickFormatter, \
    HoverTool, LabelSet
from bokeh.plotting import figure
from bokeh.models.ranges import Range1d
from django.utils import timezone

from app.coins.data import all_coins, models, filters, volumes, all_exchanges
from app.globals import pairs
from app.tools import t_s, d, spread, avg, fields, updater
from app.models import Coin, Exchange, Data, Ticker, CoinGecko, Chart, get_gecko


colors = {
    'epic-cash': 'gold',
    'grin': 'forestgreen',
    'beam': 'dodgerblue',
    'mimblewimblecoin': 'hotpink',
    'grimm': 'turquoise',
    'bitgrin': 'orangered',
    'bitcoin': "#f2a900",
    'ethereum': "black",
    'monero': "orange",
    }


def main_charts(save=False):
    ### --------- PRICE CHART

    data = {
        'time': [t_s(t) for t, p in get_gecko(models()['epic']).data['price_7d']][::2],
        'price': [p for t, p in get_gecko(models()['epic']).data['price_7d']][::2],
        }

    df = pd.DataFrame(data)
    source = ColumnDataSource(df)

    DTF = DatetimeTickFormatter()
    DTF.hours = ["%H:%M"]
    DTF.days = ["%d/%m"]
    DTF.months = ["%d/%m/%Y"]
    DTF.years = ["%d/%m/%Y"]

    TOOLS = "pan, wheel_zoom, box_zoom, reset, save"

    p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=900,
               plot_height=300, sizing_mode='scale_width')
    p.line(x='time', y='price', source=source, line_width=2, color='gold')
    p.varea(x='time', y1=0, y2='price', source=source, alpha=0.2, fill_color='gold')

    hover = HoverTool(tooltips=[
        ("Date: ", "@time{%y-%m-%d}"),
        ("Time: ", "@time{%H:%M}"),
        ("Price: ", "@price{$0.00f}")],
        formatters={"@time": "datetime",
                    'price': 'printf'},
        mode='vline')
    p.add_tools(hover)

    p.xaxis.major_label_orientation = 3.14 / 4
    p.yaxis.visible = False
    # x stuff
    p.xaxis.visible = True
    p.xgrid.visible = False
    p.xaxis.major_label_text_color = "#cccac4"
    p.xaxis[0].formatter = DTF

    # Y - PRICE
    p.y_range = Range1d(min(data['price']) * 0.9, max(data['price']) * 1.1)
    # p.yaxis.axis_label = "Price in USD"
    p.add_layout(LinearAxis(), 'right')
    p.yaxis[1].formatter = NumeralTickFormatter(format="$0.000")
    p.yaxis.major_label_text_color = "gold"

    p.ygrid.visible = False

    p.background_fill_color = None
    p.border_fill_color = None
    p.outline_line_color = None
    p.toolbar.autohide = True

    epic_7d_price, created = Chart.objects.get_or_create(name='epic_7d_price', coin=models()['epic'])
    epic_7d_price.script, epic_7d_price.div = components(p)
    epic_7d_price.updated = timezone.now()
    epic_7d_price.save()

    ### VOLUME CHART
    colors = ["#f2a900", "#459e86"]
    piles = ['Total', 'Citex', 'Vitex']
    targets = ['Bitcoin', 'USD(T)']
    vol_data = {
        'piles': piles,
        'Bitcoin': [volumes()['total']['btc'],
                    volumes()['citex']['btc'],
                    volumes()['vitex']['btc'], ],
        'USD(T)': [volumes()['total']['usdt'],
                   volumes()['citex']['usdt'],
                   0]}

    p1 = figure(x_range=piles, plot_height=50, plot_width=150,
                toolbar_location=None, tools="hover", tooltips="$name: @$name{0 a}", sizing_mode='scale_width')

    p1.vbar_stack(targets, x='piles', width=0.7, color=colors, source=vol_data,
                  legend_label=targets)

    labels = LabelSet(x='piles', y=0, text='targets', level='glyph',
                      x_offset=5, y_offset=5, source=source)

    p1.yaxis.formatter = NumeralTickFormatter(format="0,0")
    p1.ygrid.visible = False
    p1.xgrid.visible = False
    p1.legend.orientation = "horizontal"
    p1.legend.background_fill_alpha = 0
    p1.legend.border_line_color = None
    p1.background_fill_color = None
    p1.border_fill_color = None
    p1.outline_line_color = None
    p1.toolbar.autohide = True

    vol_24h, created = Chart.objects.get_or_create(name='vol_24h', coin=models()['epic'])
    vol_24h.script, vol_24h.div = components(p1)
    vol_24h.updated = timezone.now()
    vol_24h.save()

    return f'Main charts updated successfully!'


def mw_charts(save=False):
    for i, coin in enumerate(all_coins()):
        if coin.mw_coin:
            data = {
                'time': [t_s(t) for t, p in get_gecko(coin).data['price_7d']][::5],
                'price': [p for t, p in get_gecko(coin).data['price_7d']][::5],
                }

        df = pd.DataFrame(data)
        df['time'] = pd.to_datetime(df['time'])
        source = ColumnDataSource(df)

        DTF = DatetimeTickFormatter()
        DTF.hours = ["%H:%M"]
        DTF.days = ["%d/%m/'%y"]
        DTF.months = ["%d/%m/%Y"]
        DTF.years = ["%d/%m/%Y"]

        p = figure(x_axis_type="datetime", plot_width=190,
                   plot_height=45, toolbar_location=None)
        p.line(x='time', y='price', line_width=1.5, source=source, color=colors[coin.name])
        p.varea(x='time', y1=0, y2='price', alpha=0.1, source=source, fill_color=colors[coin.name])

        hover = HoverTool(tooltips=[
            ("Date: ", "@time{%y-%m-%d}"),
            ("Time: ", "@time{%H:%M}"),
            ("Price: ", "@price{$0.00f}")],
            formatters={"@time": "datetime",
                        'price': 'printf'},
            mode='vline')
        p.add_tools(hover)

        p.xaxis.major_label_orientation = 3.14 / 4
        p.yaxis.visible = False
        # x stuff
        p.xaxis.visible = False
        p.xgrid.visible = False
        p.xaxis.major_label_text_color = "grey"
        p.xaxis[0].formatter = DTF

        # Y - PRICE
        p.y_range = Range1d(min(data['price']) * 0.7, max(data['price']) * 1.1)
        # # p.yaxis.axis_label = "Price in USD"
        # p.add_layout(LinearAxis(), 'right')
        # p.yaxis[1].formatter = NumeralTickFormatter(format="$0.000")
        # p.yaxis.major_label_text_color = "gold"

        p.ygrid.visible = False

        p.background_fill_color = None
        p.border_fill_color = None
        p.outline_line_color = None
        p.toolbar.autohide = True

        mw_chart, created = Chart.objects.get_or_create(name='mw_chart', coin=coin)
        mw_chart.script, mw_chart.div = components(p)
        mw_chart.updated = timezone.now()
        mw_chart.save()

    return f'MW charts updated successfully!'


def ex_vol_chart():
    for exchange in all_exchanges():
        for target in pairs:
            data = filters()['exchanges'][exchange.name.lower()]['tickers'][target].last().candles['c7x1440']
            time = [time for time, value in data]
            value = [value for time, value in data]
            data = {'time': time, 'value': value}
            df = pd.DataFrame(data)
            df['time'] = pd.to_datetime(df['time'])
            source = ColumnDataSource(df)

            DTF = DatetimeTickFormatter()
            DTF.hours = ["%H:%M"]
            DTF.days = ["%d/%m/'%y"]
            DTF.months = ["%d/%m/%Y"]
            DTF.years = ["%d/%m/%Y"]

            p = figure(x_axis_type="datetime", plot_width=190,
                       plot_height=38, toolbar_location=None)
            p.line(x='time', y='value', line_width=1.5, source=source, color='blue')
            p.varea(x='time', y1=0, y2='value', alpha=0.1, source=source, fill_color='blue')

            hover = HoverTool(tooltips=[
                ("Date: ", "@time{%y-%m-%d}"),
                ("Time: ", "@time{%H:%M}"),
                ("Volume: ", "@value{0.00f}")],
                formatters={"@time": "datetime",
                            'price': 'printf'},
                mode='vline')
            p.add_tools(hover)

            p.xaxis.major_label_orientation = 3.14 / 4
            p.yaxis.visible = False
            p.xgrid.visible = False
            p.xaxis.major_label_text_color = "grey"
            p.xaxis[0].formatter = DTF

            # Y - PRICE
            p.y_range = Range1d(min(data['value']) * 0.8, max(data['value']) * 1.1)
            # # p.yaxis.axis_label = "Price in USD"
            # p.add_layout(LinearAxis(), 'right')
            # p.yaxis[1].formatter = NumeralTickFormatter(format="$0.000")
            # p.yaxis.major_label_text_color = "gold"

            p.ygrid.visible = False

            p.background_fill_color = None
            p.border_fill_color = None
            p.outline_line_color = None
            p.toolbar.autohide = True

            mw_chart, created = Chart.objects.get_or_create(name=f'{exchange.name} vol_7d', coin=models()['epic'])
            mw_chart.script, mw_chart.div = components(p)
            mw_chart.updated = timezone.now()
            mw_chart.save()

    return f'MW charts updated successfully!'