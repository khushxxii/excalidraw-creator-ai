import json
import uuid
import random
from typing import List, Dict, Union, Tuple, Optional, Any


class ExcalidrawElement:
    """Base class for all Excalidraw elements"""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        element_type: str,
        stroke_color: str = "#1e1e1e",
        background_color: str = "#ffffff",
        fill_style: str = "solid",
        stroke_width: int = 2,
        stroke_style: str = "solid",
        roughness: int = 1,
        opacity: int = 100,
        angle: float = 0,
        id: Optional[str] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.type = element_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.stroke_color = stroke_color
        self.background_color = background_color
        self.fill_style = fill_style
        self.stroke_width = stroke_width
        self.stroke_style = stroke_style
        self.roughness = roughness
        self.opacity = opacity
        self.seed = random.randint(1, 2000000000)
        self.version = 1
        self.version_nonce = random.randint(1, 2000000000)
        self.is_deleted = False
        self.bound_elements = []
        self.updated = int(random.random() * 10000000000)
        self.link = None
        self.locked = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert element to dictionary format for JSON serialization"""
        result = {
            "id": self.id,
            "type": self.type,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "angle": self.angle,
            "strokeColor": self.stroke_color,
            "backgroundColor": self.background_color,
            "fillStyle": self.fill_style,
            "strokeWidth": self.stroke_width,
            "strokeStyle": self.stroke_style,
            "roughness": self.roughness,
            "opacity": self.opacity,
            "groupIds": [],
            "frameId": None,
            "seed": self.seed,
            "version": self.version,
            "versionNonce": self.version_nonce,
            "isDeleted": self.is_deleted,
            "boundElements": self.bound_elements,
            "updated": self.updated,
            "link": self.link,
            "locked": self.locked
        }
        
        # Add type-specific properties
        if hasattr(self, "roundness"):
            result["roundness"] = self.roundness
            
        return result


class Text(ExcalidrawElement):
    """Text element for Excalidraw"""
    
    def __init__(
        self,
        x: float,
        y: float,
        text: str,
        font_family: str = "1",
        font_size: int = 20,
        text_align: str = "center",
        vertical_align: str = "middle",
        **kwargs
    ):
        # For text elements, width and height are calculated based on the text content and font size
        # but we set initial values that will be rendered properly by Excalidraw
        width = len(text) * (font_size * 0.6)  # Approximate width based on text length
        height = font_size * 1.2  # Approximate height based on font size
        
        # Center the text at the given coordinates
        x_centered = x - width / 2
        y_centered = y - height / 2
        
        super().__init__(x_centered, y_centered, width, height, "text", **kwargs)
        
        self.text = text
        self.font_family = font_family
        self.font_size = font_size
        self.text_align = text_align
        self.vertical_align = vertical_align
        self.base_line = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to include text-specific properties"""
        result = super().to_dict()
        result["text"] = self.text
        result["fontFamily"] = self.font_family
        result["fontSize"] = self.font_size
        result["textAlign"] = self.text_align
        result["verticalAlign"] = self.vertical_align
        result["baseline"] = self.base_line
        return result


class Rectangle(ExcalidrawElement):
    """Rectangle element for Excalidraw"""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        **kwargs
    ):
        super().__init__(x, y, width, height, "rectangle", **kwargs)
        self.roundness = {"type": 3}


class Diamond(ExcalidrawElement):
    """Diamond element for Excalidraw"""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        **kwargs
    ):
        super().__init__(x, y, width, height, "diamond", **kwargs)
        self.roundness = {"type": 2}


class Ellipse(ExcalidrawElement):
    """Ellipse element for Excalidraw"""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        **kwargs
    ):
        super().__init__(x, y, width, height, "ellipse", **kwargs)
        self.roundness = {"type": 2}


class Line(ExcalidrawElement):
    """Line element for Excalidraw"""
    
    def __init__(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        **kwargs
    ):
        # Calculate width and height based on the line endpoints
        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        super().__init__(x, y, width, height, "line", **kwargs)
        
        # Store points for the line
        self.points = [[0, 0], [x2 - x1, y2 - y1]] if x == x1 else [[x1 - x, y1 - y], [x2 - x, y2 - y]]
        
    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to include line-specific properties"""
        result = super().to_dict()
        result["points"] = self.points
        result["lastCommittedPoint"] = None
        return result


class Arrow(ExcalidrawElement):
    """Arrow element for Excalidraw"""
    
    def __init__(
        self,
        x: float,
        y: float,
        points: List[List[float]],
        start_binding: Optional[Dict] = None,
        end_binding: Optional[Dict] = None,
        elbowed: bool = True,
        roundness: Optional[Dict] = None,
        **kwargs
    ):
        # For arrows, width and height are determined by points
        width = max(p[0] for p in points) if points else 0
        height = max(p[1] for p in points) if points else 0
        
        super().__init__(x, y, width, height, "arrow", **kwargs)
        
        self.points = points
        self.start_binding = start_binding
        self.end_binding = end_binding
        self.start_arrowhead = None
        self.end_arrowhead = "arrow"
        self.elbowed = elbowed
        self.roundness = roundness
        self.fixed_segments = None
        self.start_is_special = None
        self.end_is_special = None
        
    def to_dict(self) -> Dict[str, Any]:
        """Override to_dict to include arrow-specific properties"""
        result = super().to_dict()
        result["points"] = self.points
        result["lastCommittedPoint"] = None
        result["startBinding"] = self.start_binding
        result["endBinding"] = self.end_binding
        result["startArrowhead"] = self.start_arrowhead
        result["endArrowhead"] = self.end_arrowhead
        result["elbowed"] = self.elbowed
        result["fixedSegments"] = self.fixed_segments
        result["startIsSpecial"] = self.start_is_special
        result["endIsSpecial"] = self.end_is_special
        
        if self.roundness is not None:
            result["roundness"] = self.roundness
            
        return result


class ExcalidrawCreator:
    """Class to create Excalidraw drawings programmatically"""
    
    def __init__(self, background_color: str = "#ffffff"):
        self.elements: List[ExcalidrawElement] = []
        self.background_color = background_color
    
    def add_element(self, element: ExcalidrawElement) -> ExcalidrawElement:
        """Add an element to the drawing"""
        self.elements.append(element)
        return element
    
    def add_rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        **kwargs
    ) -> Rectangle:
        """Add a rectangle to the drawing"""
        rect = Rectangle(x, y, width, height, **kwargs)
        self.add_element(rect)
        return rect
    
    def add_diamond(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        **kwargs
    ) -> Diamond:
        """Add a diamond to the drawing"""
        diamond = Diamond(x, y, width, height, **kwargs)
        self.add_element(diamond)
        return diamond
    
    def add_ellipse(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        **kwargs
    ) -> Ellipse:
        """Add an ellipse to the drawing"""
        ellipse = Ellipse(x, y, width, height, **kwargs)
        self.add_element(ellipse)
        return ellipse
    
    def add_text(
        self,
        x: float,
        y: float,
        text: str,
        font_family: str = "1",
        font_size: int = 20,
        text_align: str = "center",
        vertical_align: str = "middle",
        **kwargs
    ) -> Text:
        """Add text to the drawing
        
        Args:
            x: X-coordinate of the text center
            y: Y-coordinate of the text center
            text: The text content to display
            font_family: Font family (1=Helvetica, 2=Virgil, 3=Cascadia)
            font_size: Font size in pixels
            text_align: Text alignment (left, center, right)
            vertical_align: Vertical alignment (top, middle, bottom)
            
        Returns:
            The created Text element
        """
        text_element = Text(
            x, y, text, 
            font_family=font_family,
            font_size=font_size,
            text_align=text_align,
            vertical_align=vertical_align,
            **kwargs
        )
        self.add_element(text_element)
        return text_element
    
    def add_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        **kwargs
    ) -> Line:
        """Add a line to the drawing"""
        line = Line(x1, y1, x2, y2, **kwargs)
        self.add_element(line)
        return line
    
    def add_arrow(
        self,
        x: float,
        y: float,
        points: List[List[float]],
        **kwargs
    ) -> Arrow:
        """Add an arrow to the drawing"""
        arrow = Arrow(x, y, points, **kwargs)
        self.add_element(arrow)
        return arrow
    
    def add_curved_arrow(
        self,
        x: float,
        y: float,
        points: List[List[float]],
        start_element: Optional[ExcalidrawElement] = None,
        end_element: Optional[ExcalidrawElement] = None,
        start_binding_gap: float = 1.0,
        end_binding_gap: float = 1.0,
        **kwargs
    ) -> Arrow:
        """Add a curved arrow to the drawing
        
        Args:
            x: X-coordinate of arrow start
            y: Y-coordinate of arrow start
            points: List of points defining the arrow path
            start_element: Optional element to bind the start of the arrow to
            end_element: Optional element to bind the end of the arrow to
            start_binding_gap: Gap from the start element
            end_binding_gap: Gap from the end element
            
        Returns:
            The created Arrow element
        """
        # Create bindings if elements are provided
        start_binding = None
        end_binding = None
        
        if start_element:
            start_binding = {
                "elementId": start_element.id,
                "focus": 0.5,
                "gap": start_binding_gap
            }
            
        if end_element:
            end_binding = {
                "elementId": end_element.id,
                "focus": 0.5,
                "gap": end_binding_gap
            }
        
        # Create curved arrow with roundness
        arrow = Arrow(
            x, y, points,
            start_binding=start_binding,
            end_binding=end_binding,
            elbowed=False,  # Non-elbowed for curved arrows
            roundness={"type": 2},  # Rounded corners
            **kwargs
        )
        
        self.add_element(arrow)
        return arrow
    
    def connect_elements_with_arrow(
        self,
        start_element: ExcalidrawElement,
        end_element: ExcalidrawElement,
        **kwargs
    ) -> Arrow:
        """Connect two elements with an arrow"""
        # Calculate a simple path from start to end elements
        start_x = start_element.x + start_element.width
        start_y = start_element.y + start_element.height / 2
        
        end_x = end_element.x
        end_y = end_element.y + end_element.height / 2
        
        # Create a simple path with one midpoint
        mid_x = (start_x + end_x) / 2
        mid_y = start_y
        
        points = [
            [0, 0],  # Start point (relative to arrow x,y)
            [mid_x - start_x, mid_y - start_y],  # Mid point
            [end_x - start_x, end_y - start_y]  # End point
        ]
        
        # Create bindings to the start and end elements
        start_binding = {
            "elementId": start_element.id,
            "focus": 0.5,
            "gap": 1
        }
        
        end_binding = {
            "elementId": end_element.id,
            "focus": 0.5,
            "gap": 1
        }
        
        return self.add_arrow(
            start_x, 
            start_y, 
            points, 
            start_binding=start_binding,
            end_binding=end_binding,
            **kwargs
        )
    
    def connect_elements_with_curved_arrow(
        self,
        start_element: ExcalidrawElement,
        end_element: ExcalidrawElement,
        control_point_offset_x: float = -30,
        control_point_offset_y: float = 20,
        **kwargs
    ) -> Arrow:
        """Connect two elements with a curved arrow
        
        Args:
            start_element: The element to start the arrow from
            end_element: The element to end the arrow at
            control_point_offset_x: X offset for the control point from start point
            control_point_offset_y: Y offset for the control point from start point
            
        Returns:
            The created Arrow element
        """
        # Calculate positions
        start_x = start_element.x + start_element.width / 2
        start_y = start_element.y + start_element.height
        
        end_x = end_element.x + end_element.width / 2
        end_y = end_element.y
        
        # Create curved path with a control point
        points = [
            [0, 0],  # Start point (relative to arrow x,y)
            [control_point_offset_x, control_point_offset_y],  # Control point
            [end_x - start_x, end_y - start_y]  # End point
        ]
        
        # Create bindings to the start and end elements
        start_binding = {
            "elementId": start_element.id,
            "focus": 0.5,
            "gap": 4
        }
        
        end_binding = {
            "elementId": end_element.id,
            "focus": 0.5,
            "gap": 9
        }
        
        return self.add_curved_arrow(
            start_x, 
            start_y, 
            points, 
            start_element=start_element,
            end_element=end_element,
            start_binding=start_binding,
            end_binding=end_binding,
            **kwargs
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the drawing to a dictionary for JSON serialization"""
        return {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": [element.to_dict() for element in self.elements],
            "appState": {
                "gridSize": 20,
                "gridStep": 5,
                "gridModeEnabled": False,
                "viewBackgroundColor": self.background_color
            },
            "files": {}
        }
    
    def to_json(self, pretty: bool = True) -> str:
        """Convert the drawing to JSON string"""
        indent = 2 if pretty else None
        return json.dumps(self.to_dict(), indent=indent)
    
    def save(self, filename: str, pretty: bool = True) -> None:
        """Save the drawing to a file"""
        with open(filename, "w") as f:
            f.write(self.to_json(pretty))
    
    def group_elements(self, elements: List[ExcalidrawElement], group_id: Optional[str] = None) -> str:
        """Group elements together with a common group ID"""
        if group_id is None:
            group_id = str(uuid.uuid4())
            
        for element in elements:
            if not hasattr(element, "groupIds"):
                element.groupIds = []
            element.groupIds.append(group_id)
            
        return group_id


# Example usage
if __name__ == "__main__":
    # Create a new drawing
    drawing = ExcalidrawCreator(background_color="#f5faff")
    
    # Add a large background rectangle
    bg_rect = drawing.add_rectangle(
        100, 100, 500, 500,
        stroke_color="#364fc7",
        background_color="#a5d8ff",
        fill_style="hachure",
        roughness=2
    )
    
    # Add two smaller rectangles
    rect1 = drawing.add_rectangle(
        150, 150, 200, 200,
        stroke_color="#087f5b",
        background_color="#b2f2bb",
        fill_style="cross-hatch",
        stroke_style="dashed",
        opacity=90,
        angle=0.1
    )
    
    rect2 = drawing.add_rectangle(
        350, 250, 200, 200,
        stroke_color="#c92a2a",
        background_color="#ffc9c9",
        fill_style="cross-hatch",
        stroke_width=3,
        roughness=2,
        opacity=90,
        angle=-0.1
    )
    
    # Add some diamonds
    diamond1 = drawing.add_diamond(
        180, 180, 60, 60,
        stroke_color="#862e9c",
        background_color="#eebefa",
        roughness=0,
        angle=0.3
    )
    
    diamond2 = drawing.add_diamond(
        450, 150, 60, 60,
        stroke_color="#e67700",
        background_color="#ffec99",
        stroke_width=3,
        stroke_style="dotted",
        angle=0.5
    )
    
    # Add an ellipse
    ellipse = drawing.add_ellipse(
        350, 350, 180, 180,
        stroke_color="#5c940d",
        background_color="#d8f5a2",
        fill_style="hachure",
        stroke_width=4,
        roughness=2,
        opacity=90
    )
    
    # Add some text
    text1 = drawing.add_text(
        250, 450, "Example Drawing",
        font_size=24,
        stroke_color="#1e1e1e"
    )
    
    text2 = drawing.add_text(
        250, 480, "Created with ExcalidrawCreator",
        font_size=16,
        stroke_color="#1e1e1e"
    )
    
    # Connect elements with arrows
    arrow1 = drawing.connect_elements_with_arrow(
        rect1, rect2,
        stroke_color="#364fc7",
        background_color="#a5d8ff",
        stroke_width=3
    )
    
    arrow2 = drawing.connect_elements_with_arrow(
        rect2, rect1,
        stroke_color="#c92a2a",
        background_color="#ffc9c9",
        stroke_width=3
    )
    
    # Add a curved arrow similar to the special one in the flowchart
    curved_arrow = drawing.connect_elements_with_curved_arrow(
        rect1, diamond1,
        stroke_color="#1e1e1e",
        stroke_width=3,
        roughness=1
    )
    
    # Save the drawing to a file
    drawing.save("generated_drawing.excalidraw")
    print("Drawing saved to 'generated_drawing.excalidraw'") 