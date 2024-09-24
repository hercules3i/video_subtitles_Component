import aiohttp
import asyncio
import json
import os
class MainClass:
    async def __init__(self,data):
        self.data = data
    async def post_check(self):
        await self.post_to_drive()
    async def post_to_drive(download_data):
        url = 'https://os.3i.com.vn/MobileLogin/InsertObjectFileSubject'
        file_path = os.path.abspath(filename)
        asyncio.run(self.upload_file_async(url, file_path))

    async def post_to_drive(self):
        async with aiohttp.ClientSession() as session:
            data = {
                'video_link_original': self.data["video_link_original"],
                'video_link_edited': self.data["video_link_edited"],
                'video_content': self.data["video_content"],
            }
            url = 'https://admin.metalearn.vn/VideoBilingualEditor/InsertVideo'
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    try:
                        response_text = await response.text()
                        print("Response text:", response_text)

                        # Parse the response as JSON
                        json_response = await response.json()

                        # Debug print the entire JSON response
                        print("Full JSON response:", json_response)

                        # Extract 'object' and 'title' fields if they exist
                        object_field = json_response.get('object')
                        title_field = json_response.get('title')

                        print(f"Object: {object_field}")
                        print(f"Title: {title_field}")

                        # Trigger the custom event
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON: {e}")
                else:
                    print(f"File upload failed: {response.reason}")

    def send_custom_event(self, language, event_name, message):
        # Implement your custom event logic here
        print(f"Event triggered: {event_name} with message: {message} for language: {language}")

# Example usage:
if __name__ == '__main__':
    main_class = MainClass()
    
    asyncio.run(main_class.post_check(url, language))
