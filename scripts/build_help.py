#!/usr/bin/env python3
"""Build the in-app help view from docs/firmware-check.md.

The markdown file is the single source of the customer documentation. This script converts it to a
Simple XML view (aruba_network_insights/default/data/ui/views/firmware_help.xml) and inserts live panels at the
markers <!-- panel:NAME -->. Run it after every change of the markdown file:

    python3 scripts/build_help.py

Supported markdown: headings, paragraphs, bullet and numbered lists, tables, block quotes, fenced code,
`code`, **bold**, *italic*, [text](url). Blocks between <!-- md-only --> and <!-- /md-only --> are left out
of the view. Links that start with https://YOUR-SPLUNK/en-US/app/ become relative links inside Splunk Web.
"""
import os
import re
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "firmware-check.md")
DST = os.path.join(ROOT, "aruba_network_insights", "default", "data", "ui", "views", "firmware_help.xml")

VERSION_RE = r'"^\d+\.\d+(\.\d+){0,2}$"'

PANELS = {
    "baseline": {
        "title": "Fixed versions in use (yours first, shipped list below)",
        "query": '| inputlookup aruba_firmware_baseline_custom | eval list="yours" '
                 '| append [| inputlookup aruba_firmware_baseline | eval list="shipped"] '
                 '| table list scope train min_fixed advisory note | sort list scope train',
        "earliest": "-5m",
    },
    "issues": {
        "title": "Documented issues in use (yours first, shipped list below)",
        "query": '| inputlookup aruba_known_issues_custom | eval list="yours" '
                 '| append [| inputlookup aruba_known_issues | eval list="shipped"] '
                 '| table list model_prefix fw_from fixed_in bug_id issue | sort list model_prefix bug_id',
        "earliest": "-5m",
    },
    "validation": {
        "title": "Check of the lists (rows and typing mistakes)",
        "query": (
            '| inputlookup aruba_known_issues | eval list="Known issues (shipped)", row=bug_id." ".model_prefix, '
            'problem=mvappend(if(len(model_prefix)=0,"model_prefix is empty",null()), '
            'if(NOT match(fw_from,' + VERSION_RE + '),"fw_from is not a version such as 10.7.2.1",null()), '
            'if(len(fixed_in)>0 AND NOT match(fixed_in,' + VERSION_RE + '),"fixed_in is not a version",null()), '
            'if(len(bug_id)=0,"bug_id is empty",null()), '
            'if(NOT match(source_url,"^https://"),"source_url is not an https link",null())) '
            '| append [| inputlookup aruba_known_issues_custom | eval list="Known issues (yours)", row=bug_id." ".model_prefix, '
            'problem=mvappend(if(len(model_prefix)=0,"model_prefix is empty",null()), '
            'if(NOT match(fw_from,' + VERSION_RE + '),"fw_from is not a version such as 10.7.2.1",null()), '
            'if(len(fixed_in)>0 AND NOT match(fixed_in,' + VERSION_RE + '),"fixed_in is not a version",null()), '
            'if(len(bug_id)=0,"bug_id is empty",null()), '
            'if(NOT match(source_url,"^https://"),"source_url is not an https link",null()))] '
            '| append [| inputlookup aruba_firmware_baseline | eval list="Fixed versions (shipped)", row=scope." ".train, '
            'problem=mvappend(if(NOT match(train,"^\\d+\\.\\d+$"),"train must have two numbers such as 10.7",null()), '
            'if(NOT match(min_fixed,"^\\d+\\.\\d+\\.\\d+(\\.\\d+)?$"),"min_fixed is not a version",null()), '
            'if(NOT match(source_url,"^https://"),"source_url is not an https link",null()))] '
            '| append [| inputlookup aruba_firmware_baseline_custom | eval list="Fixed versions (yours)", row=scope." ".train, '
            'problem=mvappend(if(NOT match(train,"^\\d+\\.\\d+$"),"train must have two numbers such as 10.7",null()), '
            'if(NOT match(min_fixed,"^\\d+\\.\\d+\\.\\d+(\\.\\d+)?$"),"min_fixed is not a version",null()), '
            'if(NOT match(source_url,"^https://"),"source_url is not an https link",null()))] '
            '| eval n=1 '
            '| append [| makeresults | eval list=split("Known issues (shipped),Known issues (yours),Fixed versions (shipped),Fixed versions (yours)",",") '
            '| mvexpand list | eval n=0] '
            '| eval detail=if(isnotnull(problem),row.": ".mvjoin(problem,"; "),null()) '
            '| stats sum(n) as Rows count(detail) as "Rows with a problem" values(detail) as Problems by list '
            '| rename list as List | sort List'
        ),
        "earliest": "-5m",
    },
    "unrated": {
        "title": "Firmware that cannot be rated yet (access points of the last 30 minutes)",
        "query": '`aruba_central_index` sourcetype="aruba:central:ap" earliest=-30m '
                 '| stats latest(firmwareVersion) as firmwareVersion latest(model) as model by serialNumber '
                 '| eval scope="ap" | `aruba_fw_key` | `aruba_fw_baseline` '
                 '| where fw_status!="At or above fixed version" AND fw_status!="Below fixed version" '
                 '| stats count as APs values(model) as Models by firmwareVersion fw_train fw_status '
                 '| rename firmwareVersion as Firmware, fw_train as Train, fw_status as Status | sort - APs',
        "earliest": "-30m",
    },
}


def inline(t):
    codes = []

    def keep(m):
        codes.append("<code>%s</code>" % escape(m.group(1)))
        return "\x00%d\x00" % (len(codes) - 1)
    t = re.sub(r"`([^`]+)`", keep, t)
    t = escape(t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*\s][^*]*)\*(?![\w*])", r"<i>\1</i>", t)

    def link(m):
        url = m.group(2).replace("https://YOUR-SPLUNK/en-US/app/", "../")
        ext = url.startswith("http")
        return '<a href="%s"%s>%s</a>' % (url, ' target="_blank" rel="noopener noreferrer"' if ext else "", m.group(1))
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, t)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], t)


def table_html(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    head, body = rows[0], rows[2:]
    out = ["<table class=\"aruba-help-table\">", "<thead><tr>" + "".join("<th>%s</th>" % inline(c) for c in head) + "</tr></thead>", "<tbody>"]
    for r in body:
        out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>")
    out += ["</tbody>", "</table>"]
    return "\n".join(out)


def blocks_to_html(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
        elif l.startswith("```"):
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            out.append("<pre>%s</pre>" % escape("\n".join(lines[i + 1:j])))
            i = j + 1
        elif l.startswith("#"):
            n = len(l) - len(l.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (n, inline(l[n:].strip()), n))
            i += 1
        elif l.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            out.append(table_html(lines[i:j]))
            i = j
        elif l.startswith(">"):
            j = i
            buf = []
            while j < len(lines) and lines[j].startswith(">"):
                buf.append(lines[j][1:].strip())
                j += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(buf)))
            i = j
        elif re.match(r"^(- |\d+\. )", l):
            ordered = l[0].isdigit()
            items = []
            j = i
            while j < len(lines) and (re.match(r"^(- |\d+\. )", lines[j]) or lines[j].startswith("  ") and lines[j].strip()):
                if re.match(r"^(- |\d+\. )", lines[j]):
                    items.append(re.sub(r"^(- |\d+\. )", "", lines[j]))
                else:
                    items[-1] += " " + lines[j].strip()
                j += 1
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(x) for x in items), tag))
            i = j
        else:
            j = i
            buf = []
            while j < len(lines) and lines[j].strip() and not re.match(r"^(#|\||>|```|- |\d+\. )", lines[j]):
                buf.append(lines[j].strip())
                j += 1
            out.append("<p>%s</p>" % inline(" ".join(buf)))
            i = j
    return "\n".join(out)


def panel_xml(name):
    p = PANELS[name]
    return ("  <row>\n    <panel>\n      <title>%s</title>\n      <table>\n        <search>\n"
            "          <query>%s</query>\n          <earliest>%s</earliest>\n          <latest>now</latest>\n"
            "        </search>\n        <option name=\"count\">20</option>\n        <option name=\"drilldown\">none</option>\n"
            "      </table>\n    </panel>\n  </row>\n") % (escape(p["title"]), escape(p["query"].replace("$", "$$")), p["earliest"])


def main():
    md = open(SRC, encoding="utf-8").read()
    md = re.sub(r"<!-- md-only -->.*?<!-- /md-only -->\n?", "", md, flags=re.S)
    title = re.match(r"# (.+)\n", md).group(1)
    md = md[md.index("\n") + 1:]
    parts = re.split(r"<!-- panel:(\w+) -->\n?", md)
    xml = ['<dashboard version="1.1" theme="dark" stylesheet="firmware_help.css">',
           "  <label>Firmware check help</label>",
           "  <description>What the firmware check does, how to read it and how to maintain its data.</description>"]
    for idx, part in enumerate(parts):
        if idx % 2 == 0:
            html = blocks_to_html(part.strip())
            if html.strip():
                xml.append("  <row>\n    <panel>\n      <html>\n        <div class=\"aruba-help\">\n%s\n        </div>\n      </html>\n    </panel>\n  </row>" % html)
        else:
            xml.append(panel_xml(part).rstrip("\n"))
    xml.append("</dashboard>\n")
    open(DST, "w", encoding="utf-8").write("\n".join(xml))
    print("wrote", DST, "(%s)" % title)


if __name__ == "__main__":
    main()
