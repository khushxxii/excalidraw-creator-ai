# Excalidraw Creator

A Python toolkit for programmatically creating and generating Excalidraw diagrams from code or natural language descriptions.

## Features

- **Programmatic Diagram Creation**: Create Excalidraw diagrams directly from Python code
- **AI-Powered Generation**: Generate diagrams from natural language descriptions using AI
- **Rich Element Support**: Create rectangles, diamonds, ellipses, text, lines, and arrows
- **Element Connections**: Easily connect elements with straight or curved arrows
- **Styling Options**: Customize colors, fill styles, stroke styles, and more
- **Interactive Mode**: Run the agent in interactive conversation mode

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/excalidraw-creator.git
cd excalidraw-creator

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Using the Python Library Directly

```python
from excalidraw_creator import ExcalidrawCreator

# Create a new drawing
drawing = ExcalidrawCreator(background_color="#f5faff")

# Add some shapes
rect = drawing.add_rectangle(
    150, 150, 200, 100,
    stroke_color="#1864ab",
    background_color="#d0ebff"
)

diamond = drawing.add_diamond(
    450, 150, 150, 100,
    stroke_color="#862e9c",
    background_color="#f3d9fa"
)

# Connect with arrow
drawing.connect_elements_with_arrow(rect, diamond)

# Add text
drawing.add_text(300, 300, "My Diagram")

# Save the drawing
drawing.save("my_diagram.excalidraw")
```

### Using the AI Agent

```bash
# Generate a diagram with AI from description
python excalidraw_agent.py "Create a flowchart showing user authentication process" --output auth_flow

# Run in interactive mode
python excalidraw_agent.py --interactive
```

## Agent Features

- Break down complex drawing requests into structured plans
- Generate Python code to create the requested diagrams
- Support for multi-turn conversations in interactive mode
- Example gallery accessible through the agent

## API Overview

### ExcalidrawCreator Class

Main class for creating and managing diagrams:

- `add_rectangle(x, y, width, height, **kwargs)`: Add a rectangle
- `add_diamond(x, y, width, height, **kwargs)`: Add a diamond
- `add_ellipse(x, y, width, height, **kwargs)`: Add an ellipse
- `add_text(x, y, text, **kwargs)`: Add text
- `add_line(x1, y1, x2, y2, **kwargs)`: Add a line
- `add_arrow(x, y, points, **kwargs)`: Add an arrow
- `connect_elements_with_arrow(start_element, end_element, **kwargs)`: Connect elements
- `connect_elements_with_curved_arrow(start_element, end_element, **kwargs)`: Connect with curved arrow
- `save(filename)`: Save diagram to a file

## Examples

See `example_usage.py` for a complete example of creating a flowchart diagram programmatically.

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[MIT License](LICENSE)
