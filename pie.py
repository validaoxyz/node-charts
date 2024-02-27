import csv
from collections import Counter
import pygal
from pygal.style import Style
import re

# Define a custom style based on the original SVG
custom_style = Style(
    background='transparent',
    plot_background='transparent',
    foreground='rgba(255, 255, 255, 0.9)',
    foreground_strong='rgba(255, 255, 255, 0.9)',
    foreground_subtle='rgba(255, 255, 255, 0.9)',
    opacity='.2',
    opacity_hover='.7',
    transition='250ms ease-in',
    colors=('#f9fa00', '#01b8fe', '#59f500', '#ff3700', '#c900fe', '#780098', '#0181b2', 'grey'),  # 'grey' for "Others"
    value_font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    title_font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    label_font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    major_label_font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    legend_font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    tooltip_font_family='Consolas, "Liberation Mono", Menlo, Courier, monospace',
    value_font_size=16,
    title_font_size=16,
    label_font_size=16,
    major_label_font_size=16,
    legend_font_size=16,
    tooltip_font_size=14,
    stroke_opacity='.8',
    stroke_width=1
)


def prepare_data(counter):
    top_seven = counter.most_common(7)
    top_seven_data = [{'value': count, 'label': name} for name, count in top_seven]
    others_count = sum(count for _, count in counter.items() if _ not in dict(top_seven))
    if others_count > 0:
        top_seven_data.append({'value': others_count, 'label': 'Others'})
    return top_seven_data

def group_isps(isp_name):
    keywords = {
        r"google|gcp": "Google Cloud",
        r"ovh": "OVH",
        r"hetzner": "Hetzner",
        r"amazon": "AWS",
        r"digitalocean": "Digital Ocean",
        r"contabo": "Contabo",
        r"scaleway": "Scaleway",
        r"tencent": "Tencent",
        r"microsoft": "Microsoft"
    }
    for keyword, group_name in keywords.items():
        if re.search(keyword, isp_name, re.IGNORECASE):
            return group_name
    return isp_name  # Return the original name if no keywords match

# Read CSV and count occurrences with grouping
country_counter = Counter()
isp_counter = Counter()
version_counter = Counter()

with open('celestia.csv', mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        country_counter[row['country']] += 1
        version_counter[row['version']] += 1
        grouped_isp_name = group_isps(row['ISP'])
        isp_counter[grouped_isp_name] += 1

# Total counts for percentages
# These are now just used in the tooltip formatter
total_countries = sum(country_counter.values())
total_isps = sum(isp_counter.values())
total_versions = sum(version_counter.values())
# Prepare data for the charts
top_countries_data = prepare_data(country_counter)
top_isps_data = prepare_data(isp_counter)
top_versions_data = prepare_data(version_counter)

# Function to format the tooltip to show both percentage and raw count
def format_tooltip(value, metadata):
    total_count = metadata['total']
    percentage = (value / total_count) * 100
    return f'{percentage:.2f}% ({value} nodes)'


# Update Pie chart code to use the new data structure and tooltip formatter
country_pie_chart = pygal.Pie(style=custom_style, inner_radius=.4, show_legend=True, tooltip_fancy_mode=True)
country_pie_chart.value_formatter = lambda x: format_tooltip(x, {'total': total_countries})
for data in top_countries_data:
    country_pie_chart.add(data['label'], data['value'])
country_pie_chart.render_to_file('top_countries_pie.svg')

isp_pie_chart = pygal.Pie(style=custom_style, inner_radius=.4, show_legend=True, tooltip_fancy_mode=True)
isp_pie_chart.value_formatter = lambda x: format_tooltip(x, {'total': total_isps})
for data in top_isps_data:
    isp_pie_chart.add(data['label'], data['value'])
isp_pie_chart.render_to_file('top_isps_pie.svg')



# Pie chart for the top versions
version_pie_chart = pygal.Pie(style=custom_style, inner_radius=.4, show_legend=True, tooltip_fancy_mode=True)
version_pie_chart.value_formatter = lambda x: format_tooltip(x, {'total': total_versions})
for data in top_versions_data:
    version_pie_chart.add(data['label'], data['value'])
version_pie_chart.render_to_file('top_versions_pie.svg')

# Bar chart for the top versions
version_bar_chart = pygal.Bar(style=custom_style, show_legend=True, print_values=True, print_values_position='top')
version_bar_chart.value_formatter = lambda x: format_tooltip(x, {'total': total_versions})
for data in top_versions_data:
    version_bar_chart.add(data['label'], data['value'])
version_bar_chart.render_to_file('top_versions_bar.svg')

for data in top_versions_data:
    version_bar_chart.add(data['label'], data['value'])

# Save the chart to a file
version_bar_chart.render_to_file('top_versions_bar.svg')


# # Create a bar chart for the top countries
# country_bar_chart = pygal.Bar(style=custom_style, show_legend=True, print_values=True, print_values_position='top')
# country_bar_chart.value_formatter = lambda x: format_tooltip(x, {'total': total_countries})
# for data in top_countries_data:
#     country_bar_chart.add(data['label'], data['value'])
# country_bar_chart.render_to_file('top_countries_bar.svg')

# # Create a bar chart for the top ISPs
# isp_bar_chart = pygal.Bar(style=custom_style, show_legend=True, print_values=True, print_values_position='top')
# isp_bar_chart.value_formatter = lambda x: format_tooltip(x, {'total': total_isps})
# for data in top_isps_data:
#     isp_bar_chart.add(data['label'], data['value'])
# isp_bar_chart.render_to_file('top_isps_bar.svg')