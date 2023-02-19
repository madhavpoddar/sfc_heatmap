import numpy as np
from bokeh.models import Panel, Tabs
from bokeh.io import show

from generate_vis import vis_heatmap_sfc, vis_heatmap_basic, vis_line_chart

if __name__ == "__main__":

    # Experimental values
    # values = np.random.uniform(0, 1, size=2000)
    # values.sort()
    # values = np.concatenate((values, values[::-1]))
    # values = np.abs(np.sin(np.arange(0, 20 * np.pi, 2 * np.pi / 360)))
    # n = 12
    # values = [i / (n - 1) for i in range(n)]
    # values = [sum(values) / len(values)]

    y = [None] * 4
    y[0] = [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]
    y[1] = [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]
    y[2] = [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]
    y[3] = [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]
    N = 500
    for i, _ in enumerate(y):
        y[i] = list(np.tile(y[i], N))

    p_heatmap_sfc = vis_heatmap_sfc(
        values=y,
    )
    p_heatmap_basic = vis_heatmap_basic(
        values=y,
    )
    p_line_chart = vis_line_chart(y)

    tab1 = Panel(child=p_heatmap_sfc, title="SFC Heatmap Matrix")
    tab2 = Panel(child=p_heatmap_basic, title="Basic Heatmap Matrix")
    tab3 = Panel(child=p_line_chart, title="Line Chart")

    final_layout = Tabs(tabs=[tab1, tab2, tab3])
    show(final_layout)
