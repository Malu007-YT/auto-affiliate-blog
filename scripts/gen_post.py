from pytrends.request import TrendReq
py = TrendReq(hl='it-IT', tz=360)
trending = py.trending_searches(pn='IA')  # parole chiave calde in Italia
topic = trending.iloc[0]  # prendi il primo trend
