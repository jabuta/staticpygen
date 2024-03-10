from markdown_blocks import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ulist,
    block_type_olist,
    block_to_block_type,
    markdown_to_blocks,
)

from inline_markdown import text_to_textnodes

from htmlnode import (
    HTMLNode,
    ParentNode
)



def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_nodes.append(block_to_html_node(block))
    return ParentNode("div", block_nodes)



def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    return {
        block_type_heading: block_heading_to_html(block),
        block_type_paragraph: block_paragraph_to_html(block),
        block_type_code: block_code_to_html(block),
        block_type_quote: block_quote_to_html(block),
        block_type_ulist: block_ulist_to_html(block),
        block_type_olist: block_olist_to_html(block),
    }.get(block_type, block_paragraph_to_html(block))
    
def block_olist_to_html(block:str) -> HTMLNode:
    lis = block.splitlines()
    html_nodes = []
    for li in lis:
        li_text_nodes = text_to_textnodes(li[li.index("."):].trim())
        li_html_nodes = []
        for text_node in li_text_nodes:
            li_html_nodes.append(text_node.to_html_node())
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
    text_nodes = text_to_textnodes(block)
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
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node.to_html_node())
    return ParentNode("p", html_nodes)

def block_heading_to_html(block:str) -> HTMLNode:
    strp_block = block.strip("#")
    heading_type = len(block) - len(strp_block)
    strp_block = strp_block.trim()
    text_nodes = text_to_textnodes(strp_block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node.to_html_node())
    return ParentNode(f"h{heading_type}", html_nodes)