from agent import chat_with_customer


print("=== MemoryDesk Test ===\n")

message = input("Customer: ")

result = chat_with_customer(message)

print("\n--- AI Response ---")
print(result["answer"])

print("\n--- Memories Used ---")

if result["memories"]:
    for memory in result["memories"]:
        print("-", memory)
else:
    print("No previous memories found.")