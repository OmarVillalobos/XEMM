import plotly.graph_objects as go


fig = go.Figure()

fig.add_trace(go.Bar(
    x=["2020-01-01", "2020-04-01", "2020-07-01", "2020-10-01"],
    y=[1000, 1500, 1700,20],
    xperiod="M3",
    xperiodalignment="middle",
    xhoverformat="Q%q",
    hovertemplate="%{y}%{_xother}"
))

fig.add_trace(go.Scatter(
    x=["2020-01-01", "2020-02-01", "2020-03-01",
      "2020-04-01", "2020-05-01", "2020-06-01",
      "2020-07-01", "2020-08-01", "2020-09-01"],
    y=[1100,1050,1200,1300,1400,1700,1500,1400,1600],
    xperiod="M1",
    xperiodalignment="middle",
    hovertemplate="%{y}%{_xother}"
))

fig.update_layout(hovermode="x unified")
fig.show()