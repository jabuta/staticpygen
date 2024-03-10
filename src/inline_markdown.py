import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_image,
    text_type_link,
    text_type_bold,
    text_type_italic,
    text_type_code,
)

def text_to_textnodes(text: str) -> list[TextNode]:
    node_list = [TextNode(text,text_type_text)]
    # **split bold
    node_list = split_nodes_delimiter(node_list,"**",text_type_bold)
    # __split bold
    node_list = split_nodes_delimiter(node_list,"__",text_type_bold)
    # *split italic*
    node_list = split_nodes_delimiter(node_list,"*",text_type_italic)
    # _split italic_
    node_list = split_nodes_delimiter(node_list,"_",text_type_italic)
    # `split code
    node_list = split_nodes_delimiter(node_list,"`",text_type_code)
    node_list = split_nodes_image(node_list)
    node_list = split_nodes_link(node_list)
    return node_list

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_strings = old_node.text.split(delimiter)
        if len(split_strings) == 1 and split_strings[0] != "":
            new_nodes.append(old_node)
            continue
        if len(split_strings) % 2 == 0:
            raise ValueError("Invalid Markdown syntax: unclosed delimiter")
        for i in range(0,len(split_strings)):
            if split_strings[i] == "":
                continue
            if i % 2 == 0:
                curr_node = TextNode(split_strings[i], text_type_text)
                new_nodes.append(curr_node)
            else:
                curr_node =TextNode(split_strings[i], text_type)
                new_nodes.append(curr_node)
    return new_nodes


def split_nodes_image(nodes: list[TextNode]) -> list[TextNode]:
    node_list=[]
    for node in nodes:
        if node.text_type != text_type_text:
            node_list.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            node_list.append(node)
            continue

        text_list = node.text.split(f"![{images[0][0]}]({images[0][1]})",1)
        if text_list[0] != "":
            node_list.append(TextNode(text_list[0], text_type_text))
        node_list.append(TextNode(images[0][0], text_type_image, images[0][1]))
        for i in range(1,len(images)):
            text_list = text_list[-1].split(f"![{images[i][0]}]({images[i][1]})",1)
            if len(text_list) != 2:
                raise ValueError("Invalid markdown, link section not closed")            
            if text_list[0] != "":
                node_list.append(TextNode(text_list[0], text_type_text))
            node_list.append(TextNode(images[i][0], text_type_image, images[i][1]))

        if text_list[-1] != "":
            node_list.append(TextNode(text_list[-1], text_type_text))        
    return node_list

def split_nodes_link(nodes: list[TextNode]) -> list[TextNode]:
    node_list=[]
    for node in nodes:
        if node.text_type != text_type_text:
            node_list.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            node_list.append(node)
            continue
           
        if "![" in node.text:
            print("skipping, node contains conflicting images and links, EXTRACT IMAGES FIRST")
            node_list.append(node)
            continue

        text_list = node.text.split(f"[{links[0][0]}]({links[0][1]})",1)
        if text_list[0] != "":
            node_list.append(TextNode(text_list[0], text_type_text))
        node_list.append(TextNode(links[0][0], text_type_link, links[0][1]))
        for i in range(1,len(links)):
            text_list = text_list[-1].split(f"[{links[i][0]}]({links[i][1]})",1)
            if len(text_list) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if text_list[0] != "":
                node_list.append(TextNode(text_list[0], text_type_text))
            node_list.append(TextNode(links[i][0], text_type_link, links[i][1]))

        if text_list[-1] != "":
            node_list.append(TextNode(text_list[-1], text_type_text))        
    return node_list


def extract_markdown_images(text: str) -> list[str]:
    return re.findall( r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[str]:
    return re.findall( r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
