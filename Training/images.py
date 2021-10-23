from simple_image_download import simple_image_download as simp

def download_line_charts():
    response = simp.simple_image_download
    response().download('line chart', 500)
    line_charts = response().urls('line chart', 500)
    return line_charts

def download_bar_charts():
    response = simp.simple_image_download
    response().download('bar chart', 500)
    bar_charts = response().urls('bar chart', 500)
    return bar_charts

def download_pie_charts():
    response = simp.simple_image_download
    response().download('pie chart', 500)
    pie_charts = response().urls('pie chart', 500)
    return pie_charts

def download_scatter_charts():
    response = simp.simple_image_download
    response().download('scatter plot', 500)
    scatter_charts = response().urls('scatter plot', 500)
    return scatter_charts

def download_bubble_charts():
    response = simp.simple_image_download
    response().download('bubble chart', 500)
    bubble_charts = response().urls('bubble chart', 500)
    return bubble_charts

download_bar_charts()
download_pie_charts()
download_scatter_charts()
download_bubble_charts()



