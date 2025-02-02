import streamlit as st
from streamlit_echarts import st_echarts

from utils.math import calculate_wam, get_letter_grade_freq


def line_graph(grades):
    data = []
    for i in range(len(grades)):
        wam, _ = calculate_wam(grades[:i + 1])
        data.append(int(wam))

    min_value = min(data) - 5
    max_value = max(data) + 5

    options = {
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross",
                "label": {"backgroundColor": "#6a7985"}
            }
        },
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": [str(i + 1) for i in range(len(grades))]
        },
        "yAxis": {
            "type": "value",
            "min": min_value,
            "max": max_value
        },
        "series": [
            {
                "data": data,
                "type": "line",
                "smooth": True,
                "symbol": "none",
                "areaStyle": {
                    "color": "rgba(135, 208, 104, 0.6)",
                },
                "lineStyle": {
                    "color": "rgba(135, 208, 104, 1)",
                    "width": 2
                },
                "itemStyle": {
                    "color": "rgba(135, 208, 104, 1)"
                }
            }
        ],
    }
    st.write('### Your WAM over time')
    st_echarts(options=options, height="500px")
    st.markdown('---')


def radar_graph(grades):
    data, gmax, gmin = get_letter_grade_freq(grades)
    g_data = []
    maximum = 0
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('#### So far, you have achieved:')
        for g, f in data.items():
            if f:
                st.markdown(f"##### `{int(f)}` {g.upper()}'s")
                if f > maximum:
                    maximum = f
            g_data.append(int(f))
        st.markdown('#### Your best grade:')
        st.markdown(f'##### `{gmax}`')
        st.markdown('#### Your lowest grade:')
        st.markdown(f'##### `{gmin}`')
        st.markdown("*Don't worry, it happens :)*")
    with col2:
        option = {
            "title": {
                "textStyle": {"fontSize": 16, "fontWeight": "bold"},
                "left": "center"
            },

            "radar": {
                "indicator": [
                    {"name": "H1", "max": maximum},
                    {"name": "H2A", "max": maximum},
                    {"name": "H2B", "max": maximum},
                    {"name": "H3", "max": maximum},
                    {"name": "P", "max": maximum},
                    {"name": "N", "max": maximum},
                    {"name": "*", "max": maximum}
                ],
                "splitNumber": 5
            },
            "series": [
                {
                    "name": "Data",
                    "type": "radar",
                    "data": [
                        {
                            "value": g_data,
                            "name": "Grades by Title",
                            "areaStyle": {"color": "#87d068"}
                        }
                    ],
                }
            ],
        }
        st_echarts(option, height="500px")


def render_all_graphs(grades):
    radar_graph(grades)
    line_graph(grades)
