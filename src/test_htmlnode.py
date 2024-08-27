import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node1 = HTMLNode(
            "a",
            "a text",
            None,
            {"href": "www.google.com", "target": "_blank"}
        )

        self.assertEqual(
            ' href="www.google.com" target="_blank"',
            node1.props_to_html()
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "a text",
            None,
            {"align": "left"}
        )

        self.assertEqual(
            "HTMLNode(p, a text, None, {'align': 'left'})",
            repr(node)
        )

    def test_values(self):
        node = HTMLNode("div", "What's up doc")
        self.assertEqual("div", node.tag)
        self.assertEqual("What's up doc", node.value)
        self.assertEqual(None, node.children)
        self.assertEqual(None, node.props)


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_initialization(self):
        leaf = LeafNode(tag='p', value='Hello', props={'style': 'color:red;'})
        self.assertEqual(leaf.tag, 'p')
        self.assertEqual(leaf.value, 'Hello')
        self.assertEqual(leaf.props, {'style': 'color:red;'})

    def test_leaf_node_to_html_with_valid_value_and_tag(self):
        leaf = LeafNode(tag='p', value='Hello', props={'class': 'text'})
        expected_html = '<p class="text">Hello</p>'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_leaf_node_to_html_missing_value(self):
        # provide an empty string initially
        leaf = LeafNode(tag='p', value='', props={'class': 'text'})
        leaf.value = None
        with self.assertRaises(ValueError) as context:
            leaf.to_html()
        self.assertTrue(
            'Missing value please fackin provide one' in str(context.exception))

    def test_leaf_node_to_html_no_tag(self):
        leaf = LeafNode(None, value='Hello', props={'class': 'text'})
        self.assertEqual(leaf.to_html(), 'Hello')

    def test_leaf_node_to_html_with_props(self):
        leaf = LeafNode(tag='span', value='World', props={
                        'id': 'greeting', 'class': 'highlight'})
        expected_html = '<span id="greeting" class="highlight">World</span>'
        self.assertEqual(leaf.to_html(), expected_html)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),
                         "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()
