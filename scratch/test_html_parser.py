import re
from html.parser import HTMLParser

class SimpleMarkdownParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.in_pre = False
        self.in_code = False
        self.in_table = False
        self.table_row = []
        self.table_data = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag in ["h1", "h2", "h3", "h4"]:
            level = int(tag[1])
            self.output.append("\n\n" + "#" * level + " ")
        elif tag == "p":
            self.output.append("\n\n")
        elif tag == "pre":
            self.in_pre = True
            self.output.append("\n\n```tsx\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.output.append("`")
        elif tag == "li":
            self.output.append("\n- ")
        elif tag == "table":
            self.in_table = True
            self.table_data = []
        elif tag == "tr":
            self.table_row = []
        elif tag in ["th", "td"]:
            pass

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
            self.output.append("\n```\n\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = False
            self.output.append("`")
        elif tag == "tr" and self.in_table:
            self.table_data.append(self.table_row)
        elif tag == "table":
            self.in_table = False
            # Render markdown table
            if self.table_data:
                self.output.append("\n\n")
                # header
                header = self.table_data[0]
                self.output.append("| " + " | ".join(header) + " |\n")
                self.output.append("| " + " | ".join(["---"] * len(header)) + " |\n")
                for row in self.table_data[1:]:
                    # pad if needed
                    while len(row) < len(header):
                        row.append("")
                    self.output.append("| " + " | ".join(row[:len(header)]) + " |\n")
                self.output.append("\n")

    def handle_data(self, data):
        if self.in_table:
            clean = data.strip()
            if clean:
                if self.table_row:
                    self.table_row[-1] += " " + clean
                else:
                    self.table_row.append(clean)
        else:
            self.output.append(data)

    def get_markdown(self):
        text = "".join(self.output)
        # Clean up excessive blank lines
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()

import httpx
r = httpx.get("https://catalyst.tailwindui.com/docs/button", follow_redirects=True)
main_html = re.search(r'<main[^>]*>(.*?)</main>', r.text, re.DOTALL).group(1)

parser = SimpleMarkdownParser()
parser.feed(main_html)
md = parser.get_markdown()
print("Generated markdown snippet:\n")
print(md[:1200])
