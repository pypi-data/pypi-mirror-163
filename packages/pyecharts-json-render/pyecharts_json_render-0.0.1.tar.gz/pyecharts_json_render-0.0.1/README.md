Useage:
from pyecharts_json_render import render
jsn = render.read_json_file('./TEST_JSON.json')
render.render_html_from_ec_option_json(jsn)