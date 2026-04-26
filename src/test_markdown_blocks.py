import unittest
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        result = block_to_block_type("just some text")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading_1(self):
        result = block_to_block_type("# valid heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_2(self):
        result = block_to_block_type("## valid heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_3(self):
        result = block_to_block_type("### valid heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_4(self):
        result = block_to_block_type("#### valid heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_5(self):
        result = block_to_block_type("##### valid heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_6(self):
        result = block_to_block_type("###### valid heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_7_invalid(self):
        result = block_to_block_type("####### invalid heading")
        self.assertEqual(result, BlockType.PARAGRAPH)
    
    def test_invalid_heading(self):
        result = block_to_block_type("##2 invalid heading")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_code_block(self):
        result = block_to_block_type("```\nCool code```")
        self.assertEqual(result, BlockType.CODE)
    
    def test_code_block_invalid(self):
        result = block_to_block_type("```\nsome code\n```python")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_quote(self):
        result = block_to_block_type("> hey cool \n> \n> cool")
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_quote_invalid(self):
        result = block_to_block_type("> hey cool \n> \n cool")
        self.assertEqual(result, BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()