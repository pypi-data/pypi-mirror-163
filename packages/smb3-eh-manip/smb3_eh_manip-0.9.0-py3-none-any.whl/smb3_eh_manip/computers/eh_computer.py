from smb3_eh_manip.computers.opencv_computer import OpencvComputer
from smb3_eh_manip.settings import config, get_config_region


class EhComputer(OpencvComputer):
    def __init__(self):
        super().__init__(
            "ehvideo",
            config.get("app", "eh_video_path"),
            config.get("app", "eh_start_frame_image_path"),
            video_offset_frames=106,
            start_frame_image_region=get_config_region(
                "app", "eh_start_frame_image_region"
            ),
        )