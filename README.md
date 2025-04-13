# Excalidraw Assistant

A commandline tool for programmatically creating and generating Excalidraw diagrams from code or natural language descriptions (using the [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents))

## Features

- **AI-Powered Generation**: Generate diagrams from natural language descriptions using AI
- **Rich Element Support**: Create rectangles, diamonds, ellipses, text, lines, and arrows
- **Styling Options**: Customize colors, fill styles, stroke styles, and more
- **Interactive Mode**: Run the agent in interactive conversation mode

## Installation

```bash
# Clone (or fork) the repository
git clone https://github.com/khushxxii/excalidraw-creator.git
cd excalidraw-creator

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Using the commandline tool

```bash
# Generate a diagram with AI from description
python excalidraw_agent.py "Create a flowchart showing user authentication process" --output auth_flow

# Run in interactive mode
python excalidraw_agent.py --interactive
```

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

## Contributing

Contributions are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

[MIT License](LICENSE)
