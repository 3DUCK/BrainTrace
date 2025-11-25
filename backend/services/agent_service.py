"""
Agent Execution Service
-----------------------

This service handles the execution of external Python agents.
It runs a specified Python script in a subprocess, passing input data as JSON
and capturing the output as JSON.
"""

import logging
import subprocess
import json
import os
from typing import Dict, Any, Optional

class AgentService:
    def __init__(self, agents_dir: str = "agents"):
        """
        Initialize the AgentService.
        
        Args:
            agents_dir (str): Directory where agent scripts are located.
                              Defaults to 'agents' relative to the backend root.
        """
        # Resolve absolute path for agents directory
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.agents_dir = os.path.join(base_path, agents_dir)
        
        if not os.path.exists(self.agents_dir):
            logging.warning(f"Agents directory does not exist: {self.agents_dir}")
            os.makedirs(self.agents_dir, exist_ok=True)

    def run_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Runs a specific agent script.

        Args:
            agent_name (str): Name of the agent script (e.g., 'demo_agent.py').
            input_data (Dict[str, Any]): Input data to pass to the agent.

        Returns:
            Dict[str, Any]: The output from the agent script.
        """
        agent_path = os.path.join(self.agents_dir, agent_name)
        
        # Security check: Ensure the agent path is within the agents directory
        if not os.path.abspath(agent_path).startswith(os.path.abspath(self.agents_dir)):
            raise ValueError(f"Invalid agent path: {agent_name}")
            
        if not os.path.exists(agent_path):
            raise FileNotFoundError(f"Agent script not found: {agent_path}")

        try:
            # Serialize input data to JSON string
            input_json = json.dumps(input_data)
            
            logging.info(f"Running agent: {agent_name} with input: {input_json}")

            # Run the script using subprocess
            result = subprocess.run(
                ["python3", agent_path, input_json],
                capture_output=True,
                text=True,
                check=True,
                timeout=30 # Timeout after 30 seconds
            )
            
            # Parse output
            output_str = result.stdout.strip()
            logging.info(f"Agent output: {output_str}")
            
            try:
                output_data = json.loads(output_str)
                return output_data
            except json.JSONDecodeError:
                logging.error(f"Failed to parse agent output as JSON: {output_str}")
                return {
                    "status": "error",
                    "message": "Agent output is not valid JSON",
                    "raw_output": output_str
                }

        except subprocess.CalledProcessError as e:
            logging.error(f"Agent execution failed: {e.stderr}")
            return {
                "status": "error",
                "message": f"Agent execution failed: {e.stderr}"
            }
        except subprocess.TimeoutExpired:
            logging.error(f"Agent execution timed out: {agent_name}")
            return {
                "status": "error",
                "message": "Agent execution timed out"
            }
        except Exception as e:
            logging.error(f"Unexpected error running agent: {e}")
            return {
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            }
