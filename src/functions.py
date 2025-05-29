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
        if old_node.text.count(delimiter) >= 1 and old_node.text.count(delimiter) < 2:
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

    # Run this function on each node that is inputted, whether it's one or more
    for i in range(len(old_nodes)):

        # If the text is empty or non-existent, skip this node
        if not old_nodes[i].text or old_nodes[i].text.strip() == "":
            continue

        # Extract all the links present in the string
        links = extract_markdown_links(old_nodes[i].text)

        # If there are no links found, simply keep the string as is
        if len(links) == 0:
            new_nodes.append(TextNode(old_nodes[i].text, old_nodes[i].text_type))
            continue

        # Go through a loop for as many times as there are links found
        for v in range(len(links)):
            alt_text, url = links[v][0], links[v][1]
            
            # If it's on the first iteration of the loop, run this specific code:
            # It splits the string where the link is found, then adds the text prior to the link as well as the link
            # as nodes to the new_nodes list
            if v == 0:
                split_string = old_nodes[i].text.split(f"[{alt_text}]({url})")
                if split_string[0].strip() != "":
                    new_nodes.append(TextNode(split_string[0], TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(links[v][0], TextType.LINK, links[v][1]))
                
                # If we found the last link of the string, return the final text of the string (if it isn't empty)
                if v == len(links) - 1:
                    if split_string[1].strip() != "":
                        new_nodes.append(TextNode(split_string[1], TextType.NORMAL_TEXT))
                continue

            # If it's on any iteration after the first, this code will allow 
            # for further splitting of the second half of the string
            # It does the same thing as the previous code, just working with a different variable
            split_string = split_string[1].split(f"[{alt_text}]({url})")
            if split_string[0].strip() != "":
                new_nodes.append(TextNode(split_string[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(links[v][0], TextType.LINK, links[v][1]))

            # If we found the last link of the string, return the final text of the string (if it isn't empty)
            if v == len(links) - 1:
                    if split_string[1].strip() != "":
                        new_nodes.append(TextNode(split_string[1], TextType.NORMAL_TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []

    for i in range(len(old_nodes)):

        if not old_nodes[i].text or old_nodes[i].text.strip() == "":
            continue

        images = extract_markdown_images(old_nodes[i].text)

        if len(images) == 0:
            new_nodes.append(TextNode(old_nodes[i].text, old_nodes[i].text_type))
            continue

        for v in range(len(images)):
            alt_text, url = images[v][0], images[v][1]
            
            if v == 0:
                split_string = old_nodes[i].text.split(f"![{alt_text}]({url})")
                if split_string[0].strip() != "":
                    new_nodes.append(TextNode(split_string[0], TextType.NORMAL_TEXT))
                new_nodes.append(TextNode(images[v][0], TextType.IMAGE, images[v][1]))
                
                if v == len(images) - 1:
                    if split_string[1].strip() != "":
                        new_nodes.append(TextNode(split_string[1], TextType.NORMAL_TEXT))
                continue

            split_string = split_string[1].split(f"![{alt_text}]({url})")
            if split_string[0].strip() != "":
                new_nodes.append(TextNode(split_string[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(images[v][0], TextType.IMAGE, images[v][1]))

            if v == len(images) - 1:
                    if split_string[1].strip() != "":
                        new_nodes.append(TextNode(split_string[1], TextType.NORMAL_TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = split_nodes_delimiter(text, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes