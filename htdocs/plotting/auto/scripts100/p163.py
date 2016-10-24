import psycopg2
import numpy as np
from pandas.io.sql import read_sql
import datetime
import pytz
from collections import OrderedDict
from pyiem.plot import MapPlot
from pyiem.util import get_autoplot_context

MDICT = OrderedDict([('none', 'All LSR Types'),
                     ('nrs', 'All LSR Types except HEAVY RAIN + SNOW')])


def get_description():
    """ Return a dict describing how to call this plotter """
    d = dict()
    d['data'] = True
    d['description'] = """This application generates a map displaying the
    number of LSRs issued between a period of your choice by NWS Office."""
    today = datetime.date.today()
    jan1 = today.replace(month=1, day=1)
    d['arguments'] = [
        dict(type='datetime', name='sdate',
             default=jan1.strftime("%Y/%m/%d 0000"),
             label='Start Date / Time (UTC, inclusive):',
             min="2006/01/01 0000"),
        dict(type='datetime', name='edate',
             default=today.strftime("%Y/%m/%d 0000"),
             label='End Date / Time (UTC):',
             min="2006/01/01 0000"),
        dict(type='select', name='filter', default='all', options=MDICT,
             label='Local Storm Report Type Filter'),
    ]
    return d


def plotter(fdict):
    """ Go """
    import matplotlib
    matplotlib.use('agg')
    pgconn = psycopg2.connect(database='postgis', host='iemdb', user='nobody')
    ctx = get_autoplot_context(fdict, get_description())
    sts = ctx['sdate']
    sts = sts.replace(tzinfo=pytz.utc)
    ets = ctx['edate']
    ets = ets.replace(tzinfo=pytz.utc)
    myfilter = ctx['filter']
    tlimiter = ''
    if myfilter == 'nrs':
        tlimiter = " and typetext not in ('HEAVY RAIN', 'SNOW') "

    df = read_sql("""
    SELECT wfo, count(*) from lsrs
    WHERE valid >= %s and valid < %s """ + tlimiter + """
    GROUP by wfo ORDER by wfo ASC
    """, pgconn, params=(sts, ets), index_col='wfo')
    data = {}
    for wfo, row in df.iterrows():
        data[wfo] = row['count']
    maxv = df['count'].max()
    bins = np.linspace(0, maxv, 12, dtype='i')
    bins[-1] += 1
    p = MapPlot(sector='nws', axisbg='white',
                title='Local Storm Report Counts by NWS Office',
                subtitle=('Valid %s - %s UTC, type limiter: %s'
                          ) % (sts.strftime("%d %b %Y %H:%M"),
                               ets.strftime("%d %b %Y %H:%M"),
                               MDICT.get(myfilter)))
    p.fill_cwas(data, bins=bins, ilabel=True)

    return p.fig, df

if __name__ == '__main__':
    plotter(dict())