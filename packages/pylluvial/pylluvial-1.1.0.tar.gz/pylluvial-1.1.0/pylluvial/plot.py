from .utils import *
from .aggregate import aggregate_data
from .fit import *
from matplotlib.patches import Polygon
from typing import Hashable, Optional
import matplotlib.pyplot as plt
import numpy as np
import itertools as it


def get_flow_path(
    y1: float,
    y2: float,
    x1: float,
    x2: float,
    resolution: int = 50,
    straight_fraction: float = 0.2,
    fit: str = 'poly'
) -> tuple[np.ndarray, np.ndarray]:
    """
    compute the flow path between x1, y1 and x2, y2 using either
    a polynomial with leading and trailing straight lines or a sigmoidal

    :param y1:                  y coordinate of the first point
    :param y2:                  y coordinate of the second point
    :param x1:                  x coordinate of the first point
    :param x2:                  x coordinate of the second point
    :param resolution:          resolution of the interpolated function
    :param straight_fraction:   fraction of the space between x1 and x2 that should be straight lines for fit = 'poly'
    :param fit:                 string specifying the function to use for computing the flow path

    :return:                    numpy.ndarray, np.ndarray containing x and y coordinates of the fitted function
    """
    if fit == 'sigmoid':
        xs, ys = sigmoid_fit(
            y1, y2,
            x1, x2,
            resolution
        )

    elif fit == 'poly':
        xs, ys = poly_fit_with_straights(
            y1, y2,
            x1, x2,
            resolution,
            straight_fraction
        )

    return xs, ys


def make_flow_polygon(
    g1_strat: Stratum,
    g2_strat: Stratum,
    g1_rh: float,
    g2_rh: float,
    color: Union[str, tuple[float, float, float, float]],
    alpha: float = 1
) -> Polygon:
    """
    generates a matplotlib.patches.Polygon object for a given alluvial flow

    :param g1_strat:    origin Stratum object
    :param g2_strat:    destination Stratum object
    :param g1_rh:       flow proportion of origin Stratum
    :param g2_rh:       flow proportion of destination Stratum
    :param color:       color of the generated Polygon
    :param alpha:       opacity of the generated Polygon

    :return:            matplotlib.patches.Polygon for flow between origin and destination Stratum
    """
    y1_bottom, y1_top = g1_strat.get_flow_ycoords(g1_rh)
    y2_bottom, y2_top = g2_strat.get_flow_ycoords(g2_rh)
    x1 = g1_strat.get_right_bound(0.5)
    x2 = g2_strat.get_left_bound(0.5)
    x_bottom, y_bottom = get_flow_path(y1_bottom, y2_bottom, x1, x2)
    x_top, y_top = get_flow_path(y1_top, y2_top, x1, x2)
    x = np.concatenate([x_top, x_bottom[::-1]])
    y = np.concatenate([y_top, y_bottom[::-1]])
    flow_polygon = Polygon(
        np.array([x, y]).T,
        facecolor = color,
        edgecolor = 'white',
        alpha = alpha
    )

    return flow_polygon


def plot_group_strata(
    group_strata: list[Stratum],
    x: float,
    grouping: list[Any],
    colors: dict[Hashable, Union[str, tuple[float, float, float, float]]],
    ax: plt.Axes,
    gapsize: float = 1,
    height: float = 100,
    width: float = 0.5,
    alpha: float = 1,
    show_labels: bool = False
) -> None:
    """
    plots stratas for a given group

    :param group_strata:    list of Stratum objects
    :param x:               position of group column on x axis
    :param grouping:        list of integers indicating strata that should not have a gap between them
    :param colors:          dictionary of the form {stratum_name: color}
    :param ax:              matplotlib.Axes object to add the strata patches to
    :param gapsize:         size of gap between each pair of rectangles
    :param height:          height of the group column
    :param width:           width of the plotted rectangles
    :param alpha:           opacity of plotted rectangles
    :param show_labels:     if True, plots Stratum labels

    :return:                None
    """
    y = 0
    ngaps = len(np.unique(grouping))
    norm = Normalizer(y, height + gapsize * (ngaps - 1))
    # group_strata[::-1] is necessary to comply to top to bottom order of strata
    for i, strat_group in it.groupby(
            zip(group_strata[::-1], grouping[::-1]),
            key = lambda x: x[1]
    ):
        for stratum, _ in strat_group:
            c = colors[stratum.label]
            stratum.set_height(height, norm)
            stratum.set_width(width)
            stratum.set_xy(x, y)
            ax.add_patch(
                stratum.get_patch(c, alpha)
            )
            if show_labels:
                ax.text(
                    *stratum.get_label(),
                    rotation = 90,
                    ha = 'center',
                    va = 'center'
                )
            y += stratum.height

        y += gapsize


def plot_strata(
    strata: list[list[Stratum]],
    group_labels: list[str],
    groupings: list[list[Any]],
    strat_colors: dict[Hashable, dict[Hashable, Union[str, tuple[float, float, float, float]]]],
    stratum_width: float,
    stratum_gap: float,
    ax: plt.Axes,
    plot_height: float,
    plot_width: float,
    show_labels: bool
) -> None:
    """
    plots strata for each group

    :param strata:          list of lists of Stratum objects
    :param group_labels:    list of labels for each strata group
    :param groupings:       list of list of group labels indicating a grouping of the Stratum objects for each group
    :param strat_colors:    dictionary of the form {group_name: {stratum_name: color}}
    :param stratum_width:   width of the Stratum rectangles
    :param stratum_gap      size of the gap between strata
    :param ax:              matplotlib.Axes object to add the strata patches to
    :param plot_height:     height of the groups
    :param plot_width:      width of the plot
    :param show_labels:     if True, plots Stratum labels

    :return:                None
    """

    x = stratum_width / 2
    label_positions = []
    for group_label, group_strata, grouping in zip(group_labels, strata, groupings):
        colors = strat_colors[group_label]
        label_positions.append(x)
        plot_group_strata(
            group_strata,
            x,
            grouping,
            colors,
            ax,
            gapsize = stratum_gap,
            height = plot_height,
            width = stratum_width,
            show_labels = show_labels
        )
        x += plot_width / len(strata)

    if show_labels:
        ax.set_xticks(label_positions)
        ax.set_xticklabels(group_labels)

    ax.set_xlim(0, x - plot_width / len(strata) + stratum_width / 2)
    ax.set_ylim(0, plot_height)


def plot_flows(
    strata: list[list[Stratum]],
    lodes: list[list[np.ndarray]],
    ax: plt.Axes
) -> None:
    """
    plot flows between strata

    :param strata:  list of lists of Stratum objects
    :param lodes:   list of lists of numpy.ndarrays holding the Stratum flow proportions (see also get_lodes)
    :param ax:      matplotlib.Axes object to add the flows to

    :return:        None
    """
    for (i, g1_strats), (_, g2_strats) in pairwise(enumerate(strata)):
        for j, g1_strat in enumerate(g1_strats):
            relative_widths = lodes[i][j]
            for k, g2_strat in enumerate(g2_strats):
                flow_polygon = make_flow_polygon(
                    g1_strat,
                    g2_strat,
                    relative_widths[k][0],
                    relative_widths[k][1],
                    g1_strat.color
                )
                ax.add_patch(flow_polygon)

        # reset lode_position for next round
        reset_strata(g2_strats)


def alluvial(
    x: Union[str, Iterable],
    stratum: Union[str, Iterable],
    alluvium: Union[str, Iterable],
    palette: str = 'husl',
    hue: Optional[Union[str, Iterable]] = None,
    data: Optional[pd.DataFrame] = None,
    ax: Optional[plt.Axes] = None,
    stratum_width: float = 2,
    stratum_gap: float = 1,
    plot_height: float = 100,
    plot_width: float = 150,
    show_labels: bool = False
) -> Union[plt.Axes, tuple[plt.Figure, plt.Axes]]:
    """
    generate alluvial plot. x, stratum and alluvium are either strings if data is given or iterables of same length
    containing the data to plot in long format (e.g. [0, 0, 1, 1, 2, 2], [0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1]).
    In the latter case hue also has to be an iterable of the same length

    :param x:               string denoting the column to use for grouping of data if data is given else iterable
    :param stratum:         string denoting the column to use for computing stata heights if data is given else iterable
    :param alluvium:        string denoting the column to use for computing flows between strata if data is given else iterable
    :param palette:         string denoting a given seaborn palette or dictionary of the form {'group_name': {'statum_name': 'color'}}
    :param hue:             string denoting the column to use for computing Stratum splits if data else iterable
    :param data:            pandas.DataFrame containing data in long format
    :param ax:              matplotlib.Axes object to generate the plot in
    :param stratum_width:   width of the stratum rectangles to plot
    :param stratum_gap:     gap between strata in a group
    :param plot_height:     height of the generated plot
    :param plot_width:      width of the generated plot
    :param show_labels:     if True plots Stratum name with each Stratum

    :return:                matplotlib.Axes if ax is given else matplotlib.Figure, matplotlib.Axes
    """
    return_fig = False
    if not ax:

        fig, ax = plt.subplots()
        return_fig = True

    if not isinstance(data, pd.DataFrame):
        data = to_dataframe(x, alluvium, stratum, hue = hue)
        x = 'x'
        stratum = 'stratum',
        alluvium = 'alluvium'
        hue = 'hue'

    data = data.copy()
    if hue:
        for col in [stratum, hue]:
            data.loc[:, col] = data.loc[:, col].astype(str)

        data['grouping'] = data.loc[:, stratum]
        data.loc[:, stratum] = data[[stratum, hue]].agg('_'.join, axis = 1)

    else:
        data['grouping'] = data.loc[:, stratum]

    colors = get_color_dict(
        data,
        x,
        stratum,
        hue = hue,
        sns_palette = palette
    )

    strata, lodes, group_labels, groupings = aggregate_data(
        data,
        x,
        alluvium,
        stratum
    )

    plot_strata(
        strata,
        group_labels,
        groupings,
        colors,
        stratum_width,
        stratum_gap,
        ax,
        plot_height,
        plot_width,
        show_labels = show_labels
    )

    plot_flows(
        strata,
        lodes,
        ax
    )

    if not show_labels:
        ax.set_xticks([])

    ax.set_yticks([])
    for pos in ['top', 'bottom', 'left', 'right']:
        ax.spines[pos].set_visible(False)

    return ax if not return_fig else (fig, ax)