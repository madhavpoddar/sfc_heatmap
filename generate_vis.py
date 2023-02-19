from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, LinearColorMapper, ColorBar, Span
from bokeh.transform import linear_cmap
from matplotlib import cm
from matplotlib.colors import rgb2hex
import alphashape

from shapely.geometry import mapping

import numpy as np
from generate_sfc import get_sfc


def split(a, n):
    k, m = divmod(len(a), n)
    a_split = list(a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))

    # for i in range(len(a_split)):
    #     a_split[i].append(a_split[(i + 1) % len(a_split)][0])
    return a_split


def vis_line_chart(values):
    p = figure(
        height=250,
        width=1250,
        x_range=(-1, len(values[0])),
    )
    max_values = max([max(vs) for vs in values])
    min_values = min([min(vs) for vs in values])

    yaxis_labels = {}
    for i, values_one_row in enumerate(values):
        p.varea(
            x=range(len(values_one_row)),
            y1=[i - 0.45] * len(values_one_row),
            y2=i
            - 0.45
            + 0.9 * (np.array(values_one_row) - min_values) / (max_values - min_values),
        )
        h_span = Span(location=i - 0.45, dimension="width")
        p.renderers.extend(
            [
                h_span,
            ]
        )
        yaxis_labels[i] = "y[" + str(i) + "]"
    p.yaxis.ticker = list(yaxis_labels.keys())
    p.yaxis.major_label_overrides = yaxis_labels
    return p


def vis_heatmap_sfc(
    values,
    n_columns: int = 25,
    cmap_value_range: dict = None,
    level: int = 6,
    line_width: int = 1,
    add_boundry_line: bool = False,
    add_padding: bool = False,
    xaxis_labels=None,
):

    p = figure(
        height=250,
        width=1250,
        x_range=(0, n_columns),
        y_range=(0, (len(values) - 1) * 1.1 + 1)
        # match_aspect=True,
    )
    if xaxis_labels is None:
        xaxis_labels = {}
        for i, split_range in enumerate(split(list(range(len(values[0]))), n_columns)):
            xaxis_labels[i + 0.5] = str(min(split_range)) + "-" + str(max(split_range))
    p.xaxis.ticker = list(xaxis_labels.keys())
    p.xaxis.major_label_overrides = xaxis_labels
    p.xaxis.major_label_orientation = "vertical"

    yaxis_labels = {}
    for i in range(len(values)):
        yaxis_labels[i * 1.1 + 0.5] = "y[" + str(i) + "]"
    p.yaxis.ticker = list(yaxis_labels.keys())
    p.yaxis.major_label_overrides = yaxis_labels

    xp_orig = None
    yp_orig = None

    if cmap_value_range is None:
        cmap_value_range = {
            "low": min([min(values_1_row) for values_1_row in values]),
            "high": max([max(values_1_row) for values_1_row in values]),
        }

    for row_index, values_1_row in enumerate(values):
        for col_index, values_1_cell in enumerate(split(values_1_row, n_columns)):

            val = values_1_cell

            if xp_orig is None:
                while True:
                    xp_orig, yp_orig = get_sfc(
                        level=level, add_padding=add_padding, sfc_type="hilbert"
                    )
                    if len(xp_orig) >= len(val):
                        break
                    level += 1
                    print(
                        "Increasing SFC level by 1 (Too many data points based)... New level: ",
                        level,
                    )

            xp = list(xp_orig + col_index)
            yp = list(yp_orig + row_index * 1.1)

            # Alternate Sequence: For testing purpose only
            # val = [0, 1] * int(len(xp) / 2)

            if add_boundry_line:
                p.line(
                    xp,
                    yp,
                    line_color="black",
                    line_width=line_width + 1,
                )

            split_n = len(val)
            xp_split_list = split(xp, split_n)
            yp_split_list = split(yp, split_n)
            sfc_multi_line_cds = ColumnDataSource(
                data=dict(
                    xs=xp_split_list,
                    ys=yp_split_list,
                    val=val,
                )
            )

            cmap = LinearColorMapper(
                palette="Cividis256",
                low=cmap_value_range["low"],
                high=cmap_value_range["high"],
            )

            p.multi_line(
                source=sfc_multi_line_cds,
                xs="xs",
                ys="ys",
                line_color={"field": "val", "transform": cmap},
                line_width=line_width,
            )

            # TODO: Add this feature later if required
            #  For subdividing SFCs to improve readability
            # if draw_tick_layer:
            # cmap = LinearColorMapper(palette="Inferno256", low=0, high=len(val))
            # p.multi_line(
            #     source=sfc_multi_line_cds,
            #     xs="xs",
            #     ys="ys",
            #     line_color={"field": "val", "transform": cmap},
            #     line_width=line_width,
            #     line_alpha=0.2,
            # )
            # p.multi_line(
            #     source=sfc_multi_line_cds,
            #     xs="xs",
            #     ys="ys",
            #     line_color="black",
            #     line_width=line_width,
            #     alpha="val",
            # )
            # for (xp_split, yp_split) in zip(xp_split_list, yp_split_list):
            #     # draw convex boundary
            #     alpha_shape_poly = alphashape.alphashape(list(zip(xp_split, yp_split)), 0.0)
            #     poly_mapped = mapping(alpha_shape_poly)

            #     if len(list(poly_mapped["coordinates"][0])) == 1:
            #         print(list(poly_mapped["coordinates"][0]))
            #     xp, yp = zip(*(list(poly_mapped["coordinates"][0])))

            #     p.patch(
            #         x=list(xp),
            #         y=list(yp),
            #         fill_color=None,
            #         line_color="black",
            #         line_width=3,
            #     )
    cb = ColorBar(color_mapper=cmap, label_standoff=12)
    p.add_layout(cb, "right")
    return p


def vis_heatmap_basic(
    values,
    n_columns: int = 25,
    cmap_value_range: dict = None,
):
    xaxis_labels = {}
    for i, split_range in enumerate(split(list(range(len(values[0]))), n_columns)):
        xaxis_labels[i + 0.5] = str(min(split_range)) + "-" + str(max(split_range))
    if cmap_value_range is None:
        cmap_value_range = {
            "low": min([min(values_1_row) for values_1_row in values]),
            "high": max([max(values_1_row) for values_1_row in values]),
        }
    values_aggregated = [None] * len(values)
    for row_index, values_1_row in enumerate(values):
        values_aggregated[row_index] = [None] * n_columns
        for col_index, values_1_cell in enumerate(split(values_1_row, n_columns)):
            values_aggregated[row_index][col_index] = sum(values_1_cell) / len(
                values_1_cell
            )

    return vis_heatmap_sfc(
        values=values_aggregated,
        n_columns=n_columns,
        cmap_value_range=cmap_value_range,
        xaxis_labels=xaxis_labels,
    )
