from agents.supervisor import create_supervisor_agent


if __name__ == "__main__":
    supervisor = create_supervisor_agent()
    
    # Test Case 1: Single domain request (weather)
    query1 = "What is the weather in Tokyo?"
    for step in supervisor.stream(
        {"messages": [{"role": "user", "content": query1}]}
    ):
        for update in step.values():
            for message in update.get("messages", []):
                message.pretty_print()
    
    # print("\n")
    
    # Test Case 2: Single domain request (country)
    # print("=" * 60)
    # print("Test 2: Country Information Request")
    # print("=" * 60)
    # query2 = "Tell me about Germany"
    # for step in supervisor.stream(
    #     {"messages": [{"role": "user", "content": query2}]}
    # ):
    #     for update in step.values():
    #         for message in update.get("messages", []):
    #             message.pretty_print()
    
    # print("\n")
    
    # Test Case 3: Complex multi-domain request
    # print("=" * 60)
    # print("Test 3: Multi-Domain Request")
    # print("=" * 60)
    # query3 = "Tell me about Italy and what's the weather like in Rome?"
    # for step in supervisor.stream(
    #     {"messages": [{"role": "user", "content": query3}]}
    # ):
    #     for update in step.values():
    #         for message in update.get("messages", []):
    #             message.pretty_print()