from textnode import TextNode, TextType

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
        split_node = old_node.text.split(delimiter)
        for i in range(0, len(split_node)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node[i], TextType.NORMAL_TEXT))
            else:
                new_nodes.append(TextNode(split_node[i], delimiter_type))
    return new_nodes
        
        
        

"""
    For each old node:
    If the text type is NOT normal text, simply add it to the new nodes list and move on
    If it is normal, search for the delimiter, split the sentence starting there and ending after the next delimiter,
    and append those sentences to the new_nodes list. But the sentences have to be converted into a TextNode object.
    The delimiter words would be textnodes with the textype of the delimiter. The non-delimiter words would be texttypes of normal text.

"""