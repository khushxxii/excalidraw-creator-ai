import os
import asyncio
import tempfile
import sys
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

# Load environment variables
load_dotenv()

# Ensure excalidraw_creator is available
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from excalidraw_creator import ExcalidrawCreator
except ImportError:
    print("Error: excalidraw_creator.py must be in the same directory as this script.")
    sys.exit(1)


@function_tool
async def analyze_and_plan(description: str) -> str:
    """
    Breaks down a drawing request into digestible parts and creates a structured plan.
    
    Args:
        description: A natural language description of what to draw
    
    Returns:
        A structured plan for creating the drawing
    """
    # Create a thinking agent to break down the request
    thinking_agent = Agent(
        name="ExcalidrawPlanner",
        instructions="""
        You are an analytical assistant that breaks down complex drawing tasks into simpler components.
        
        When given a description of something to draw, your job is to:
        1. Identify all the main elements that need to be drawn
        2. For each element, list the appropriate Excalidraw shapes to use
        3. Consider the spatial relationships and connections between elements
        4. Create a step-by-step plan for implementing the drawing
        5. Suggest appropriate colors, styles, and effects
        
        Be thorough but concise in your analysis.
        """,
        model="gpt-4o",
    )
    
    # Generate the plan
    plan_result = await Runner.run(
        thinking_agent,
        input=f"""
        I need to create an Excalidraw diagram of: {description}
        
        Please break this down into:
        1. Main elements to draw
        2. Appropriate shapes for each element
        3. Spatial layout and relationships
        4. Color scheme and styling recommendations
        5. Step-by-step implementation plan
        """
    )
    
    return plan_result.final_output


@function_tool
async def generate_python_script(description: str, script_name: str, plan: Optional[str] = None) -> str:
    """
    Generates a Python script that creates an Excalidraw diagram based on the description.
    
    Args:
        description: A natural language description of what to draw
        script_name: The name of the Python script to generate (without .py extension)
        plan: Optional structured plan from analyze_and_plan tool
    
    Returns:
        A message confirming the script was created
    """
    try:
        # Prepare the input with the plan if provided
        code_gen_input = f"""Generate Python code that uses the ExcalidrawCreator to draw: {description}
        
        The code should:
        1. Import the ExcalidrawCreator module using: from excalidraw_creator import ExcalidrawCreator
        2. Create the appropriate elements based on the description
        3. Save the result to a file named '{script_name}.excalidraw'
        4. Be well-commented and easy to understand
        
        IMPORTANT: Return only the raw Python code without any markdown formatting or code block delimiters.
        DO NOT include ```python or ``` tags in your response."""
        
        if plan:
            code_gen_input = f"""Generate Python code that uses the ExcalidrawCreator to draw: {description}
            
            Here's a structured plan to follow:
            {plan}
            
            The code should:
            1. Import the ExcalidrawCreator module using: from excalidraw_creator import ExcalidrawCreator
            2. Create the appropriate elements based on the plan above
            3. Save the result to a file named '{script_name}.excalidraw'
            4. Be well-commented and easy to understand
            
            IMPORTANT: Return only the raw Python code without any markdown formatting or code block delimiters.
            DO NOT include ```python or ``` tags in your response."""
        
        # Use another agent to generate the Python code
        code_gen_agent = Agent(
            name="ExcalidrawCodeGenerator",
            instructions="""
            You are an expert Python programmer specializing in creating Excalidraw diagrams.
            
            Your job is to generate Python code that uses the ExcalidrawCreator class to create 
            Excalidraw diagrams based on natural language descriptions.
            
            IMPORTANT: You must use the following import statement EXACTLY:
            ```
            from excalidraw_creator import ExcalidrawCreator
            ```
            
            The ExcalidrawCreator has these main methods:
            - add_rectangle(x, y, width, height, **kwargs)
            - add_ellipse(x, y, width, height, **kwargs)
            - add_diamond(x, y, width, height, **kwargs)
            - add_line(x1, y1, x2, y2, **kwargs)
            - add_arrow(x, y, points, **kwargs)
            - connect_elements_with_arrow(start_element, end_element, **kwargs)
            - save(filename): Saves the drawing to a file
            
            All elements support these common parameters:
            - stroke_color: Color of the outline (e.g., "#1e1e1e")
            - background_color: Fill color (e.g., "#f8d8b9")
            - fill_style: "solid", "hachure", "cross-hatch"
            - stroke_width: Line thickness (e.g., 2)
            - stroke_style: "solid", "dashed", "dotted"
            - roughness: 0 (smooth) to 2 (rough)
            - opacity: 0-100 (percentage)
            - angle: Rotation in radians
            
            To create a drawing, you would typically:
            1. Create an instance: drawing = ExcalidrawCreator()
            2. Add elements: rect = drawing.add_rectangle(...)
            3. Save the result: drawing.save("filename.excalidraw")
            
            If provided with a structured plan, follow it closely to implement the drawing.
            
            IMPORTANT: Provide complete, working Python code WITHOUT any markdown formatting or code block delimiters.
            Do NOT include ```python or ``` tags in your response - just provide the raw code.
            """,
            model="gpt-4o",
        )
        
        # Generate Python code for the Excalidraw creation
        code_result = await Runner.run(
            code_gen_agent, 
            input=code_gen_input
        )
        
        python_code = code_result.final_output
        
        # Remove any markdown code block formatting if present
        python_code = re.sub(r'^```(?:python)?', '', python_code, flags=re.MULTILINE)
        python_code = re.sub(r'```$', '', python_code, flags=re.MULTILINE)
        python_code = python_code.strip()
        
        # Ensure correct import statement 
        if "from excalidraw import" in python_code:
            python_code = python_code.replace("from excalidraw import", "from excalidraw_creator import")
        if "import excalidraw" in python_code:
            python_code = python_code.replace("import excalidraw", "import excalidraw_creator")
        
        # Save the generated code to a Python file
        script_filename = f"{script_name}.py"
        with open(script_filename, 'w') as f:
            f.write(python_code)
        
        # Now run the generated script to create the Excalidraw file
        result = os.system(f"python3 {script_filename}")
        if result != 0:
            return f"Error: Failed to run the generated script. Please check {script_filename} for errors."
        
        return f"""
        Success! I've created two files:
        
        1. {script_filename}: The Python script that generates the diagram
        2. {script_name}.excalidraw: The Excalidraw file containing your diagram
        
        You can view the Excalidraw file by opening it in Excalidraw, or you can 
        modify the Python script to make further changes.
        """
    except Exception as e:
        return f"Error generating script: {str(e)}"


@function_tool
async def list_available_excalidraw_examples() -> str:
    """
    Lists available examples of Excalidraw diagrams that can be created.
    
    Returns:
        A description of available example diagrams
    """
    return """
    Here are some examples of what you can create:
    
    1. Basic shapes: Rectangles, ellipses, diamonds, lines, and arrows with various styles and colors
    2. Flowcharts: Connected boxes showing a process flow
    3. Diagrams: Technical diagrams with labeled components
    4. People: Stick figures or cartoon-style people in various poses
    5. Scenes: Simple scenes with multiple elements (like a house with trees)
    6. Mind maps: Connected concepts with a central idea
    
    For each, you can customize colors, sizes, positions, and styles.
    """


class ExcalidrawAgentRunner:
    def __init__(self):
        self.agent = Agent(
            name="ExcalidrawCreator",
            instructions="""
            You are an assistant that helps users create Excalidraw diagrams from natural language descriptions.
            
            You can generate Python scripts that use the ExcalidrawCreator library to create diagrams based on
            the user's description. Your goal is to accurately interpret what the user wants to draw and 
            create a Python script that will generate the appropriate Excalidraw file.
            
            IMPORTANT: Always follow this process when handling a request:
            1. FIRST, use the analyze_and_plan tool to break down the drawing request into a clear plan
            2. THEN, use the generate_python_script tool with both the description and the plan
            
            This two-step approach ensures that even complex drawings are properly structured.
            For simple requests, the plan can be brief but should still identify the main elements.
            
            When users provide a description, first clarify if necessary, then follow the process above.
            """,
            tools=[analyze_and_plan, generate_python_script, list_available_excalidraw_examples],
            model="gpt-4o",
        )
    
    async def process_request(self, user_input: str) -> str:
        """Process a user request and return the agent's response"""
        try:
            result = await Runner.run(self.agent, input=user_input)
            return result.final_output
        except Exception as e:
            return f"Error processing request: {str(e)}"


async def main():
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Create Excalidraw diagrams from natural language')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('description', nargs='?', help='Description of what to draw')
    parser.add_argument('--output', default='diagram', help='Output filename (without extension)')
    parser.add_argument('--show-plan', action='store_true', help='Show the planning step in the output')
    args = parser.parse_args()
    
    runner = ExcalidrawAgentRunner()
    
    if args.interactive:
        print("Excalidraw Generator (press Ctrl+C to exit)")
        print("--------------------------------------")
        
        while True:
            try:
                description = input("\nWhat would you like to draw? ")
                if description.lower() in ['exit', 'quit', 'q']:
                    break
                    
                print("\nGenerating your diagram...")
                print("First, analyzing and planning...")
                response = await runner.process_request(description)
                print("\n" + response + "\n")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
    
    elif args.description:
        print(f"Creating a diagram of: {args.description}")
        print(f"Output will be saved as: {args.output}.excalidraw\n")
        print("First, analyzing and planning...")
        
        response = await runner.process_request(
            f"Create a diagram of {args.description} and save it as {args.output}"
        )
        print(response)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main()) 