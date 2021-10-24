import os
import requests
import shutil
import time

class MediaAPI:
  REQUEST_HEADERS = {
        "x-api-key": os.environ["DOLBYIO_API_KEY"],
        "Content-Type": "application/json",
        "Accept": "application/json",
  }

  def prepare_media(self, file_path, dolby_input_url):
    file_path = file_path
    
    url = "https://api.dolby.com/media/input"
    body = {
        "url": dolby_input_url,
    }

    response = requests.post(url, json=body, headers=self.REQUEST_HEADERS)
    response.raise_for_status()
    data = response.json()
    presigned_url = data["url"]

    print("Uploading {0} to {1}".format(file_path, presigned_url))
    with open(file_path, "rb") as input_file:
      requests.put(presigned_url, data=input_file)

  def check_job_status(self, job_id, endpoint_url):
    url = endpoint_url
    params = {
        "job_id": job_id,
    }

    try:
        response = requests.get(url, params=params, headers=self.REQUEST_HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception(response.text)

    return response.json()

  def download_media(self, output_path, transcoded_media_url):
    url = "https://api.dolby.com/media/output"
    args = {
        "url": transcoded_media_url,
    }

    with requests.get(url, params=args, headers=self.REQUEST_HEADERS, stream=True) as response:
        response.raise_for_status()
        response.raw.decode_content = True
        print("\nDownloading from {0} into {1}".format(response.url, output_path))
        with open(output_path, "wb") as output_file:
            shutil.copyfileobj(response.raw, output_file)

  def transcode(self, dolby_input_url, transcoded_media_url, output_path, request_body):
    url = "https://api.dolby.com/media/transcode"

    try:
        response = requests.post(url, json=request_body, headers=self.REQUEST_HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise Exception(response.text)

    job_id = response.json()["job_id"]

    print("\nTranscoding your media file...")
    print("Job ID >>> ", job_id)

    # check job status every 10 seconds and download transcoded file when complete
    while True:
      job_response = self.check_job_status(job_id, url)
      job_status = job_response["status"]

      if (job_status and job_status == "Success"):
        return self.download_media(output_path, transcoded_media_url)
      else:
        print(job_response)
        time.sleep(10)

  def diagnose(self, file_path, dolby_input_url):
    self.prepare_media(file_path, dolby_input_url)

    url = "https://api.dolby.com/media/diagnose"
    body = {
        "input"  : dolby_input_url,
    }

    response = requests.post(url, json=body, headers=self.REQUEST_HEADERS)
    response.raise_for_status()

    job_id = response.json()["job_id"];

    print("\nDiagnosing your media file...")
    print("Job ID >>> ", job_id)

    # check job status every 10 seconds and return media info diagnosis when complete
    while True:
      job_response = self.check_job_status(job_id, url)
      job_status = job_response["status"]

      if (job_status and job_status == "Success"):
        print("\nMedia Info >>>", job_response["result"]["media_info"])
        return job_response["result"]["media_info"]
      else:
        print(job_response)
        time.sleep(10)
