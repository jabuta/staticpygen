import re

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

