import requests
import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-u', type=str, required=False, help='Target URL')
parser.add_argument('-l', type=str, required=False, help='File containing list of URLS')
parser.add_argument('-o', type=str, required=False, help='File to write output')
parser.add_argument('-silent', action='store_true', help='Enable silent mode', required=False, default=False)

args = parser.parse_args()

variable_names_pattern = r'var\s+([a-zA-Z_$][\w$]*)'
const_names_pattern = r'const\s+([a-zA-Z_$][\w$]*)'
let_names_pattern = r'let\s+([a-zA-Z_$][\w$]*)'
input_name_pattern = r'<input.*?name="(.*?)".*?>'
input_id_pattern = r'<input.*?id="(.*?)".*?>'
object_name_pattern = r'\{\s*([^{}&()\/\s,:]+?):'
url_parameters_pattern = r'\?(.*?)='

unique_output = []

domains = []


if args.u:
    domains.append(args.u)
if args.l:
    with open(args.l, 'r') as f:
        domains.extend(f.read().splitlines())

for domain in domains:
    req = requests.get(domain)
    content = req.text


    def variable_names(pattern, content):   
        variable_names = re.findall(pattern, content)
        [unique_output.append(x) for x in variable_names if x not in unique_output]

    def const_names(pattern, content):
        const_names = re.findall(pattern, content)
        [unique_output.append(x) for x in const_names if x not in unique_output]

    def let_names(pattern, content):
        let_names = re.findall(pattern, content)
        [unique_output.append(x) for x in let_names if x not in unique_output]

    def input_name(pattern, content):
        input_name = re.findall(pattern, content)
        [unique_output.append(x) for x in input_name if x not in unique_output]

    def input_id(pattern, content):
        input_id = re.findall(pattern, content)
        [unique_output.append(x) for x in input_id if x not in unique_output]
    def object_name(pattern, content):
        object_name = re.findall(pattern, content)
        [unique_output.append(x.replace('"', '').replace("'", '')) for x in object_name if x not in unique_output]

    def url_parameters(pattern, content):
        urls = re.findall(r'<a[^>]*?href="(https?://[^"]*?)"', content)
        for url in urls:   
            params = re.findall(pattern, url)
            if params:
                [unique_output.append(x) for x in params if x not in unique_output]

    variable_names(variable_names_pattern, content)
    const_names(const_names_pattern, content)
    let_names(let_names_pattern, content)
    input_name(input_name_pattern, content)
    input_id(input_id_pattern, content)
    object_name(object_name_pattern, content)
    url_parameters(url_parameters_pattern, content)

    for parameters in unique_output:
        if not args.silent:
            print(parameters)
        if args.o:
            with open(args.o, 'a') as o:
                o.write(parameters + "\n")

