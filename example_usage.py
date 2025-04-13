from excalidraw_creator import ExcalidrawCreator

# Create a new Excalidraw drawing
drawing = ExcalidrawCreator(background_color="#f0f9ff")

# Create a flowchart-like diagram
# Start with a header rectangle
header = drawing.add_rectangle(
    300, 100, 200, 80,
    stroke_color="#1864ab",
    background_color="#d0ebff",
    fill_style="solid",
    stroke_width=2,
    roughness=0,
    opacity=100
)

# Add process steps
process1 = drawing.add_rectangle(
    150, 250, 180, 100,
    stroke_color="#2b8a3e",
    background_color="#d3f9d8",
    fill_style="solid",
    stroke_width=2,
    roughness=0,
    opacity=100
)

process2 = drawing.add_rectangle(
    450, 250, 180, 100,
    stroke_color="#e67700",
    background_color="#fff3bf",
    fill_style="solid",
    stroke_width=2,
    roughness=0,
    opacity=100
)

# Add a decision diamond
decision = drawing.add_diamond(
    300, 400, 200, 150,
    stroke_color="#862e9c",
    background_color="#f3d9fa",
    fill_style="solid",
    stroke_width=2,
    roughness=0,
    opacity=100
)

# Add result rectangle
result = drawing.add_rectangle(
    300, 600, 200, 80,
    stroke_color="#c92a2a",
    background_color="#ffe3e3",
    fill_style="solid",
    stroke_width=2,
    roughness=0,
    opacity=100
)

# Connect elements with arrows
drawing.connect_elements_with_arrow(
    header, process1,
    stroke_color="#1864ab",
    stroke_width=2
)

drawing.connect_elements_with_arrow(
    header, process2,
    stroke_color="#1864ab",
    stroke_width=2
)

drawing.connect_elements_with_arrow(
    process1, decision,
    stroke_color="#2b8a3e",
    stroke_width=2
)

drawing.connect_elements_with_arrow(
    process2, decision,
    stroke_color="#e67700",
    stroke_width=2
)

drawing.connect_elements_with_arrow(
    decision, result,
    stroke_color="#862e9c",
    stroke_width=2
)

# Save the drawing to a file
drawing.save("flowchart_example.excalidraw")
print("Flowchart saved to 'flowchart_example.excalidraw'") 