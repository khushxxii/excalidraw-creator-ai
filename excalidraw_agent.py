import os
import asyncio
import tempfile
import sys
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool

# Import prompts
from prompts import (
    PLANNER_INSTRUCTIONS,
    CODE_GENERATOR_INSTRUCTIONS,
    MAIN_AGENT_INSTRUCTIONS,
    ANALYSIS_PLAN_TEMPLATE,
    CODE_GEN_TEMPLATE_WITH_PLAN,
    CODE_GEN_TEMPLATE_WITHOUT_PLAN,
    AVAILABLE_EXAMPLES
)

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
        instructions=PLANNER_INSTRUCTIONS,
        model="gpt-4o",
    )
    
    # Generate the plan
    plan_result = await Runner.run(
        thinking_agent,
        input=ANALYSIS_PLAN_TEMPLATE.format(description=description)
    )
    
    # Log the plan to the console
    print("\nPlan for drawing:")
    print("----------------")
    print(plan_result.final_output)
    print("----------------\n")
    
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
        if plan:
            code_gen_input = CODE_GEN_TEMPLATE_WITH_PLAN.format(
                description=description,
                plan=plan,
                script_name=script_name
            )
        else:
            code_gen_input = CODE_GEN_TEMPLATE_WITHOUT_PLAN.format(
                description=description,
                script_name=script_name
            )
        
        # Use another agent to generate the Python code
        code_gen_agent = Agent(
            name="ExcalidrawCodeGenerator",
            instructions=CODE_GENERATOR_INSTRUCTIONS,
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
        
        # (HARDCODED) Ensure correct import statement 
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
    return AVAILABLE_EXAMPLES


class ExcalidrawAgentRunner:
    def __init__(self):
        self.agent = Agent(
            name="ExcalidrawCreator",
            instructions=MAIN_AGENT_INSTRUCTIONS,
            tools=[analyze_and_plan, generate_python_script, list_available_excalidraw_examples],
            model="gpt-4o",
        )
        self.conversation_history = []  # Store conversation history
    
    async def process_request(self, user_input: str) -> str:
        """Process a user request and return the agent's response"""
        try:
            # If there's conversation history, use it for context
            if self.conversation_history:
                # Create input with conversation history plus new user message
                new_input = self.conversation_history + [{"role": "user", "content": user_input}]
                result = await Runner.run(self.agent, input=new_input)
            else:
                # First message in conversation
                result = await Runner.run(self.agent, input=user_input)
            
            # Update conversation history with the result for next turn
            self.conversation_history = result.to_input_list()
            
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
    args = parser.parse_args()
    
    runner = ExcalidrawAgentRunner()
    
    if args.interactive:
        print("Excalidraw Generator (press Ctrl+C to exit)")
        print("--------------------------------------")
        print("Type 'reset' to start a new conversation, or 'exit'/'quit'/'q' to exit")
        
        while True:
            try:
                description = input("\nWhat would you like to draw? ")
                if description.lower() in ['exit', 'quit', 'q']:
                    break
                
                if description.lower() == 'reset':
                    runner.conversation_history = []
                    print("Conversation history has been reset.")
                    continue
                
                has_history = bool(runner.conversation_history)
                print("\nGenerating your diagram..." + (" (with conversation context)" if has_history else ""))
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