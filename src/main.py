import json
from media_api import MediaAPI
from transcode_request_body import Input, Output, Audio, Video, TranscodeRequestBody

# returns the recommended video bitrate for SDR uploads given the video's frame rate and resolution
def get_recommended_bitrate(frame_rate: int, resolution: int):
  is_standard_frame_rate = frame_rate <= 30 and frame_rate >= 24
  is_high_frame_rate = frame_rate <= 60 and frame_rate >= 30

  if (is_standard_frame_rate):
    return {
      2160: 45000,
      1440: 16000,
      1080: 8000,
      720: 5000,
      480: 2500,
      360: 1000
    }[resolution]
  elif (is_high_frame_rate):
    return {
      2160: 68000,
      1440: 24000,
      1080: 12000,
      720: 7500,
      480: 4000,
      360: 1500
    }[resolution]
  
  return None

if __name__ == "__main__":
  # local directory for the video you want to transcode
  file_path = "./pre-transcoded-video.mp4"
  # where should dobly.io temporarily store the video you want to transcode?
  dolby_input_url = "dlb://in/pre-transcoded-video.mp4"
  # where should dobly.io temporarily store the output of your transcoded video?  
  transcoded_media_url = "dlb://out/transcoded-video.mp4"
  # where do you want to locally store the transcoded video output?
  output_path = "./transcoded-video.mp4" 

  media_api = MediaAPI()
  media_info = media_api.diagnose(file_path, dolby_input_url)

  audio_object = Audio(
    codec = "aac_lc",
    bitrate_kb = 384,
    channels = 2
  )

  video_object = Video(
    codec = "h264",
    width = media_info["video"]["width"],
    height = media_info["video"]["height"],
    frame_rate = media_info["video"]["frame_rate"],
    bitrate_mode = "vbr",
    # use original video bitrate if get_recommended_bitrate() returns None
    # original video bitrate shouldn't be greater than 1000001
    bitrate_kb = get_recommended_bitrate(
      frame_rate = media_info["video"]["frame_rate"],
      resolution = media_info["video"]["height"]
    ) or min(media_info["video"]["bitrate"], 1000001)
  )
  
  input_object = Input(dolby_input_url)
  
  output_object = Output(
    destination = transcoded_media_url,
    kind = "mp4",
    audio = audio_object,
    video = video_object
  )

  transcode_request_body = TranscodeRequestBody(
    [input_object], 
    [output_object]
  )

  transcode_request_body = json.loads(
    json.dumps(transcode_request_body, default=lambda o: o.__dict__)
  )
  
  media_api.transcode(
    dolby_input_url, 
    transcoded_media_url, 
    output_path, 
    transcode_request_body
  )
