"""AWS Architecture Center grouping colours.

Matches the nested boxes in AWS reference architecture diagrams:
AWS Cloud → Account → Region → VPC → AZ → Subnet.
https://aws.amazon.com/architecture/icons/
"""

CLOUD = {
    "bgcolor": "transparent",
    "pencolor": "#FF9900",
    "style": "rounded",
    "penwidth": "2",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "14",
    "fontname": "Sans-Serif",
    "margin": "16",
}

ACCOUNT = {
    "bgcolor": "#FFF8F0",
    "pencolor": "#E87722",
    "style": "dashed,rounded",
    "penwidth": "1.6",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "13",
    "fontname": "Sans-Serif",
}

REGION = {
    "bgcolor": "#F9F0F5",
    "pencolor": "#BD0F72",
    "style": "dashed,rounded",
    "penwidth": "1.5",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "12",
    "fontname": "Sans-Serif",
}

VPC = {
    "bgcolor": "#F1F8E9",
    "pencolor": "#248814",
    "style": "rounded",
    "penwidth": "2",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "12",
    "fontname": "Sans-Serif",
}

AZ = {
    "bgcolor": "#FFFFFF",
    "pencolor": "#7AA116",
    "style": "dashed,rounded",
    "penwidth": "1.2",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "11",
    "fontname": "Sans-Serif",
}

PUBLIC_SUBNET = {
    "bgcolor": "#C8E6C9",
    "pencolor": "#1D8900",
    "style": "rounded",
    "penwidth": "1.2",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "11",
    "fontname": "Sans-Serif",
}

PRIVATE_SUBNET = {
    "bgcolor": "#BBDEFB",
    "pencolor": "#147EBA",
    "style": "rounded",
    "penwidth": "1.2",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "11",
    "fontname": "Sans-Serif",
}

GROUP = {
    "bgcolor": "#FAFAFA",
    "pencolor": "#545B64",
    "style": "rounded",
    "penwidth": "1",
    "labeljust": "l",
    "labelloc": "t",
    "fontsize": "11",
    "fontname": "Sans-Serif",
}

GRAPH = {
    "fontsize": "18",
    "fontname": "Sans-Serif",
    "bgcolor": "white",
    "pad": "0.35",
    "splines": "spline",
    "nodesep": "0.40",
    "ranksep": "0.55",
    "compound": "true",
}

NODE = {
    "fontname": "Sans-Serif",
    "fontsize": "10",
}

EDGE = {
    "fontname": "Sans-Serif",
    "fontsize": "9",
    "color": "#545B64",
}
