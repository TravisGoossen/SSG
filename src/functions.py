from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == "`":
        delimiter_type = TextType.CODE_TEXT
    elif delimiter == "**":
        delimiter_type = TextType.BOLD_TEXT
    elif delimiter == "_":
        delimiter_type = TextType.ITALIC_TEXT
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        if old_node.text.count(delimiter) < 2:
            raise Exception(f"Invalid markdown: One or more delimiters are missing from the string. Delimiter = '{delimiter}'")
        split_node = old_node.text.split(delimiter)
        for i in range(0, len(split_node)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.NORMAL_TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], delimiter_type))
    return new_nodes
        
        
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_link(old_nodes):
    new_nodes = []
    for i in range(len(old_nodes)):
        links = extract_markdown_links(old_nodes[i].text)
        for i in range(len(links)):
            pass
    