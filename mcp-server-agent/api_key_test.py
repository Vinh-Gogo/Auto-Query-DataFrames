import anthropic
import os
import time

# Thay thế YOUR_ANTHROPIC_API_KEY bằng API key thực tế của bạn
api_key = ""
client = anthropic.Anthropic(api_key=api_key)

message_batch = client.beta.messages.batches.create(
    requests=[
        {
            "custom_id": "first-prompt-in-my-batch",
            "params": {
                "model": "claude-3-haiku-20240229",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hey Claude, tell me a short fun fact about video games!",
                    }
                ],
            },
        },
        {
            "custom_id": "second-prompt-in-my-batch",
            "params": {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hey Claude, tell me a short fun fact about bees!",
                    }
                ],
            },
        },
    ]
)
print(f"Batch ID: {message_batch.id}")

while message_batch.processing_status == "in_progress":
    print("Batch is still processing...")
    time.sleep(5)  # Chờ một khoảng thời gian trước khi kiểm tra lại
    message_batch = client.beta.messages.batches.retrieve(message_batch.id)

print(f"Batch status: {message_batch.processing_status}")
if message_batch.processing_status == "succeeded":
    # Lấy kết quả từ results_url (nếu có) hoặc thông qua các phương thức khác
    print(f"Results URL: {message_batch.results_url}")
    # Bạn có thể cần gọi một API khác để lấy kết quả chi tiết của từng request
    # Ví dụ (có thể cần điều chỉnh theo API của Anthropic):
    # for request_result in client.beta.messages.batches.results(message_batch.id):
    #     print(f"Result for {request_result.custom_id}: {request_result.response.content[0].text}")
else:
    print(f"Batch failed or expired. Status: {message_batch.processing_status}")

print(message_batch)


