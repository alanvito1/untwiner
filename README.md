# untwiner

This is a simple Python package for loading and navigating [Twine 2](https://twinery.org/) story files.

From twinery.org:
> Twine is an open-source tool for telling interactive, nonlinear stories.

## Status

Now the code is under development, in a state of early alpha. The current format of Harlowe 3 stories is supported. You can download a story from an HTML file, view file information, get nodes and follow the links in them.
Scripting inside stories is not parsed, other formats were not checked.

## Install

```bash
pip install git+https://github.com/terentjew-alexey/untwiner.git
```

## Using

```python
# init
from untwiner import Untwiner
story = Untwiner('/path/to/my_story.html')

# some info
print(story.title)
print(story.format)
print(story.format_version)
print(story.creator)
print(story.creator_version)

# getting the start node, its text, links to the following nodes
start_node = story.start_node()
print(start_node.text)
print(start_node.media)
print(start_node.links)

# navigating
next_node = story[start_node.links[0]]
next_node = story[start_node.links[0].target]
next_node = story.node_by_id(2)
next_node = story.node_by_name('target_node_title')
next_node = story.node_by_link(start_node.links[0])

# getting nodes by tags
node_list = story.nodes_by_tags(['story_tag', 'my_tag'])
```
