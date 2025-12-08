#!/usr/bin/env python3

import requests
import mimetypes
from config import Config


class CloudFlareR2:


    def __init__(self):

        self.config = Config()
        self.cloudflare_account_id = self.config.CLOUDFLARE_ACCOUNT_ID
        self.cloudflare_bucket_name = self.config.CLOUDFLARE_BUCKET_NAME
        self.cloudflare_api_token = self.config.CLOUDFLARE_API_TOKEN


    def list_r2_objects(self):

        r2_objects_list = []
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account_id}/r2/buckets/{self.cloudflare_bucket_name}/objects"
        headers = {
            "Authorization": f"Bearer {self.cloudflare_api_token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()

            if data.get("success"):
                for obj in data.get("result", []):
                    r2_objects_list.append({
                        "key": obj.get("key"),
                        "size": obj.get("size"),
                        "contentType": obj.get("http_metadata", {}).get("contentType")
                    })
            else:
                print("Failed to retrieve objects. Errors:", data.get("errors"))
                pass
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            pass

        print(f"Successfully retrieved {len(r2_objects_list)} objects from R2 bucket '{self.cloudflare_bucket_name}'.")
        return r2_objects_list


    def upload_r2_object(self, file_path, object_key):
        
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account_id}/r2/buckets/{self.cloudflare_bucket_name}/objects/{object_key}"
        
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        headers = {
            "Authorization": f"Bearer {self.cloudflare_api_token}",
            "Content-Type": content_type
        }

        try:
            with open(file_path, 'rb') as f:
                response = requests.put(url, headers=headers, data=f)
                response.raise_for_status()
                
                data = response.json()
                
                if data.get("success"):
                    print(f"Successfully uploaded '{file_path}' to R2 as '{object_key}'.")
                else:
                    print(f"Failed to upload '{file_path}' to R2 as '{object_key}'.")
                    print("Errors:", data.get("errors"))
                    
        except FileNotFoundError:
            print(f"Error: File not found at '{file_path}'")
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
