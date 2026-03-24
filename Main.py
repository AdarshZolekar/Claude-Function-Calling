"""
Claude AI Function Calling - Improved Demo
Demonstrates multi-tool use (function calling) with the Claude API.
"""

import os
import json
from anthropic import Anthropic
from tools import TOOLS, dispatch_tool
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
MODEL = "claude-sonnet-4-5"


def run_conversation(user_message: str) -> str:
    """
    Runs a full conversation turn with tool-use support.
    Handles multi-step tool calls until Claude produces a final text response.
    """
    print(f"\n👤 User: {user_message}")
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        # Collect all tool-use blocks
        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

        if response.stop_reason == "tool_use" and tool_use_blocks:
            # Append Claude's full response (may contain text + tool_use blocks)
            messages.append({"role": "assistant", "content": response.content})

            # Build a single tool_results block for all requested tool calls
            tool_results = []
            for block in tool_use_blocks:
                print(f"\n🔧 Calling tool: {block.name}({block.input})")
                result = dispatch_tool(block.name, block.input)
                print(f"   → Result: {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            messages.append({"role": "user", "content": tool_results})

        else:
            # Final text response
            text_blocks = [b.text for b in response.content if hasattr(b, "text")]
            final_reply = " ".join(text_blocks).strip()
            print(f"\n🤖 Claude: {final_reply}")
            return final_reply


def main():
    demo_prompts = [
        "I scored 0.72 on my exam. Did I pass?",
        "What is 1337 multiplied by 42?",
        "What's the weather like in Mumbai right now?",
        "I got 0.45 on my test. Also, what's 256 divided by 8?",
    ]

    print("=" * 60)
    print("  Claude AI — Multi-Tool Function Calling Demo")
    print("=" * 60)

    for prompt in demo_prompts:
        run_conversation(prompt)
        print("-" * 60)


if __name__ == "__main__":
    main()
