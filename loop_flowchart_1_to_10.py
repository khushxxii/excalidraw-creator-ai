from excalidraw_creator import ExcalidrawCreator

# Create an Excalidraw drawing instance
drawing = ExcalidrawCreator()

# Draw the Start Terminator
start = drawing.add_ellipse(
    x=100, y=50, width=100, height=50,
    stroke_color="#1e1e1e", background_color="#b9f8b9", fill_style="solid",
    stroke_width=2, stroke_style="solid", roughness=0, opacity=100
)
drawing.add_text(x=150, y=75, text="Start")

# Draw Initialization Process Block
init = drawing.add_rectangle(
    x=100, y=150, width=100, height=50,
    stroke_color="#1e1e1e", background_color="#b9d8f8", fill_style="solid",
    stroke_width=2, stroke_style="solid", roughness=0, opacity=100
)
drawing.add_text(x=150, y=175, text="i = 1")

# Draw the Decision Block
decision = drawing.add_diamond(
    x=100, y=250, width=120, height=70,
    stroke_color="#1e1e1e", background_color="#f8f8b9", fill_style="solid",
    stroke_width=2, stroke_style="solid", roughness=0, opacity=100
)
drawing.add_text(x=150, y=285, text="i <= 10")

# Draw the Print Process Block
print_block = drawing.add_rectangle(
    x=300, y=250, width=100, height=50,
    stroke_color="#1e1e1e", background_color="#b9d8f8", fill_style="solid",
    stroke_width=2, stroke_style="solid", roughness=0, opacity=100
)
drawing.add_text(x=350, y=275, text="print(i)")

# Draw the Increment Process Block
increment = drawing.add_rectangle(
    x=300, y=350, width=100, height=50,
    stroke_color="#1e1e1e", background_color="#b9d8f8", fill_style="solid",
    stroke_width=2, stroke_style="solid", roughness=0, opacity=100
)
drawing.add_text(x=350, y=375, text="i = i + 1")

# Draw the End Terminator
end = drawing.add_ellipse(
    x=100, y=450, width=100, height=50,
    stroke_color="#1e1e1e", background_color="#f8b9b9", fill_style="solid",
    stroke_width=2, stroke_style="solid", roughness=0, opacity=100
)
drawing.add_text(x=150, y=475, text="End")

# Draw the Connector Arrows
drawing.connect_elements_with_arrow(start, init, stroke_color="#1e1e1e", stroke_width=3)
drawing.connect_elements_with_arrow(init, decision, stroke_color="#1e1e1e", stroke_width=3)
drawing.connect_elements_with_arrow(decision, print_block, stroke_color="#1e1e1e", stroke_width=3, opacity=100, stroke_style="solid")
drawing.connect_elements_with_arrow(print_block, increment, stroke_color="#1e1e1e", stroke_width=3)
drawing.connect_elements_with_arrow(increment, decision, stroke_color="#1e1e1e", stroke_width=3)
drawing.connect_elements_with_arrow(decision, end, stroke_color="#1e1e1e", stroke_width=3, angle=3.14)

# Save the drawing
drawing.save("loop_flowchart_1_to_10.excalidraw")