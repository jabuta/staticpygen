import re

from inline_markdown import text_to_textnodes

from htmlnode import (
    HTMLNode,
    ParentNode
)

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"

def block_to_block_type(block: str) -> str:
    if re.match("^#{1,6} ", block):
        return block_type_heading
    if block.startswith("```") and block.endswith("```"):
        return block_type_code
    if block.startswith(">"):
        if len([line for line in block.split("\n") if line[0] != ">" ]) == 0:
            return block_type_quote
    if block.startswith("* ") or block.startswith("- "):
        if len([line for line in block.split("\n") if not (line.startswith("* ") or line.startswith("- "))]) == 0:
            return block_type_ulist
    if block[0].isdigit():
        try:
            number_loc = block.index(".") - 1
            if len([line for line in block.split("\n") if line[0:number_loc].isdigit() ]) == 0:
                return block_type_olist
        except:
            pass
    return block_type_paragraph
    

def markdown_to_blocks(markdown: str) -> list[str]:
    return [ block.strip() for block in re.split("\n{2,}", markdown) if block.strip() != "" ]


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        convert_func = block_to_html_node(block)
        block_nodes.append(convert_func(block))
    return ParentNode("div", block_nodes)



def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    return {
        block_type_heading: block_heading_to_html,
        block_type_paragraph: block_paragraph_to_html,
        block_type_code: block_code_to_html,
        block_type_quote: block_quote_to_html,
        block_type_ulist: block_ulist_to_html,
        block_type_olist: block_olist_to_html,
    }.get(block_type)
    
def block_olist_to_html(block:str) -> HTMLNode:
    lis = block.splitlines()
    html_nodes = []
    for li in lis:
        li_text_nodes = text_to_textnodes(li[(li.index(".")+2):])
        li_html_nodes = []
        for text_node in li_text_nodes:
            li_html_nodes.append(text_node.to_html_node())
        html_nodes.append(ParentNode("li",li_html_nodes))
    return ParentNode("ol", html_nodes)

def block_ulist_to_html(block:str) -> HTMLNode:
    lis = block.splitlines()
    html_nodes = []
    for li in lis:
        li_text_nodes = text_to_textnodes(li[2:])
        li_html_nodes = []
        for text_node in li_text_nodes:
            li_html_nodes.append(text_node.to_html_node())
        html_nodes.append(ParentNode("li", li_html_nodes))
    return ParentNode("ul", html_nodes)

def block_quote_to_html(block:str) -> HTMLNode:
    strp_block = block.lstrip("> ").replace("\n> "," ")
    text_nodes = text_to_textnodes(strp_block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node.to_html_node())
    return ParentNode("blockquote", html_nodes)

def block_code_to_html(block:str) -> HTMLNode:
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node.to_html_node())
    return ParentNode("code", [ ParentNode("pre", html_nodes)])

def block_paragraph_to_html(block:str) -> HTMLNode:
    text_nodes = text_to_textnodes(block.replace("\n"," "))
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node.to_html_node())
    return ParentNode("p", html_nodes)

def block_heading_to_html(block:str) -> HTMLNode:
    strp_block = block.lstrip("#")
    heading_type = len(block) - len(strp_block)
    strp_block = strp_block.strip()
    text_nodes = text_to_textnodes(strp_block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node.to_html_node())
    return ParentNode(f"h{heading_type}", html_nodes)