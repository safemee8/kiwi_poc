from enum import Enum
from typing import List, Dict

from pydantic import BaseModel, Field
from datetime import datetime, timezone


class PydanticBaseModel(BaseModel):
    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }


class BaseEnum(Enum):
    @classmethod
    def list(cls):
        values = [member.value for role, member in cls.__members__.items()]
        return values


class MeetingStatusEnum(str, BaseEnum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    WAITING = "WAITING"


class MeetingUserTypeEnum(str, BaseEnum):
    owner = "owner"
    moderator = "moderator"
    participant = "participant"
    public = "public"


class MeetingTypeEnum(str, BaseEnum):
    conference = "conference"
    webinar = "webinar"
    live_class = "live_class"
    live_streaming = "live_streaming"
    audio_call = "audio_call"
    talk_to_me = "talk_to_me"
    live_call = "live_call"
    direct_call = "direct_call"


class TransactionalTypeEnum(str, BaseEnum):
    audio_call = "audio_call"
    talk_to_me = "talk_to_me"
    live_call = "live_call"


class MeetingSourceTypeEnum(str, BaseEnum):
    user = "user"
    email = "email"
    api = "api"
    garbage_collector = "garbage_collector"


class DurationModeEnum(str, BaseEnum):
    hr = "hr"
    min = "min"


class MeetingSourceModel(PydanticBaseModel):
    source: MeetingSourceTypeEnum
    identifier: str


class ParticipantSessionModel(PydanticBaseModel):
    start_time: int = 0
    end_time: int = 0


class ParticipantsModel(PydanticBaseModel):
    token: str = ""
    attended: bool = False
    sessions: Dict[str, ParticipantSessionModel] = None
    time_in_meeting: int = 0


class EventsModel(PydanticBaseModel):
    description: str
    created_on: int


class CoBrowsingsModel(PydanticBaseModel):
    start_request_time: int = 0
    end_request_time: int = 0
    co_browsing_duration: int = 0


class RecordingsModel(PydanticBaseModel):
    start_request_time: int = 0
    end_request_time: int = 0
    recording_duration: int = 0
    size_bytes: int = 0
    download_link: str = ""
    format: str = ""


class StreamingsReqModel(PydanticBaseModel):
    stream_url: str


class StreamingsModel(PydanticBaseModel):
    start_request_time: int = 0
    end_request_time: int = 0
    streaming_duration: int = 0
    stream_url: str = ""


class StakeHolderExperienceModel(PydanticBaseModel):
    can_show_camera: bool = False
    can_speak: bool = False
    can_screen_share: bool = False
    can_collaborate: bool = False
    can_document_share: bool = False
    can_record: bool = False
    can_stream: bool = False
    can_video_share: bool = False
    can_start_meeting: bool = False
    can_end_meeting: bool = False
    can_kick_out: bool = False
    can_chat: bool = False
    can_raise_hand: bool = False
    can_mute_everyone: bool = False
    can_secure: bool = False
    can_see_stats: bool = False
    can_invite: bool = False
    can_co_browse: bool = False
    is_video_on: bool = False
    is_audio_on: bool = False


class MeetingExperienceModel(PydanticBaseModel):
    owner: StakeHolderExperienceModel
    public: StakeHolderExperienceModel
    moderator: StakeHolderExperienceModel
    participant: StakeHolderExperienceModel


class MeetingsReqModel(PydanticBaseModel):
    moderators: List[str] = Field([], title="moderators", description="List of moderator identifiers as string")
    participants: List[str] = Field([], title="participants", description="List of participant identifiers as string")
    date: str = Field("", title="date", description="Data in mm/dd/yyyy format. eg. 09/28/2020 for Sep 28, 2020")
    time: str = Field("", title="time", description="Data in HH:MM p format. eg. 10:30 AM")
    timezone: str = Field("", title="timezone", description="Timezone for date/time. eg. Asia/Kolkata")
    duration: int = Field(1, title="duration", description="Meeting duration mentioned as multiplier to duration_mode")
    duration_mode: DurationModeEnum = Field(DurationModeEnum.hr, title="Duration_mode", description="this is a block of time that along with duration multiplier gives meeting length. eg. 2 hr. 2 is duration and 'hr' is duration_mode")
    watermark: str = Field("", title="watermark", description="Watermark image url for watermark to be shown in meeting window")
    rrule: str = Field("", title="rrule", description="Standard rrule format string that mentions meeting recurrance")
    is_recurring: bool = Field(False, title="is_recurring", description="Flag for recurring meetings")
    auto_record: bool = Field(False, title="auto_record", description="Flag to automatically start recording on this meeting. This flag overrides auto_record_meetings in organization model")
    end_recurring: int = Field(0, title="end_recurring", description="Time in milliseconds since epoch beyond which recurring meetings will not be scheduled. Default: sets itself to last meeting in recurring rrule.")
    room_name: str = Field("", title="room_name", description="Has to be amongst room_names in organization or user room_name. Leave empty for random room name")
    meeting_name: str = Field("", title="meeting_name", description="Meeting name that appears in communication.")
    description: str = Field("", title="description", description="Meeting description that appears in communication.")
    meeting_password: str = Field("", title="meeting_password", description="Password to be passed in meetings.")
    meeting_type: MeetingTypeEnum = Field(title="meeting_type", description="This field is a plan type to use for creating this meeting.")
    can_co_browse: bool = Field(False, title="can_co_browse", description="Flag to allow co-browsing in meeting.")


class MeetingsUpdateModel(PydanticBaseModel):
    moderators: List[str] = Field(..., title="moderators", description="List of moderator identifiers as string")
    participants: List[str] = Field(..., title="participants", description="List of participant identifiers as string")
    date: str = Field(..., title="date", description="Data in mm/dd/yyyy format. eg. 09/28/2020 for Sep 28, 2020")
    time: str = Field(..., title="time", description="Data in HH:MM p format. eg. 10:30 AM")
    timezone: str = Field(..., title="timezone", description="Timezone for date/time. eg. Asia/Calcutta")
    duration: int = Field(..., title="duration", description="Meeting duration mentioned as multiplier to duration_mode")
    duration_mode: DurationModeEnum = Field(..., title="Duration_mode", description="this is a block of time that along with duration multiplier gives meeting length. eg. 2 hr. 2 is duration and 'hr' is duration_mode")
    watermark: str = Field(..., title="watermark", description="Watermark image url for watermark to be shown in meeting window")
    rrule: str = Field(..., title="rrule", description="Standard rrule format string that mentions meeting recurrance")
    is_recurring: bool = Field(..., title="is_recurring", description="Flag for recurring meetings")
    auto_record: bool = Field(..., title="auto_record", description="Flag to automatically start recording on this meeting. This flag overrides auto_record_meetings in organization model")
    end_recurring: int = Field(..., title="end_recurring", description="Time in milliseconds since epoch beyond which recurring meetings will not be scheduled. Default: sets itself to last meeting in recurring rrule.")
    room_name: str = Field(..., title="room_name", description="Has to be amongst room_names in organization or user room_name. Leave empty for random room name")
    meeting_name: str = Field(..., title="meeting_name", description="Meeting name that appears in communication.")
    description: str = Field(..., title="description", description="Meeting description that appears in communication.")
    meeting_password: str = Field(..., title="meeting_password", description="Password to be passed in meetings.")
    meeting_type: MeetingTypeEnum = Field(..., title="meeting_type", description="This field is a plan type to use for creating this meeting.")
    can_co_browse: bool = Field(False, title="can_co_browse", description="Flag to allow co-browsing in meeting.")


class MeetingsTableModel(MeetingsReqModel):
    id: str
    created_by_user_id: str
    recording_url: str = ""
    events: List[EventsModel] = []
    tokens: Dict[str, ParticipantsModel] = {}
    recurring_batch_id: str = ""
    start_time: int = 0
    end_time: int = 0
    run_time: int = 0
    recording_time: int = 0
    streaming_time: int = 0
    start_by: MeetingSourceModel = None
    end_by: MeetingSourceModel = None
    cumulative_participant_time: int = 0
    scheduled_time: int = 0
    meeting_status: MeetingStatusEnum = MeetingStatusEnum.SCHEDULED
    participant_count: int = 0
    public_session_count: int = 0
    co_browsing_time: int = 0
    client_id: str
    co_browsings: List[CoBrowsingsModel] = []
    recordings: List[RecordingsModel] = []
    streamings: List[StreamingsModel] = []
    participant_durations: Dict[str, int] = {}
    created_on: int
    updated_on: int


class MeetingsResponseModel(MeetingsReqModel):
    id: str
    created_by_user_id: str
    recording_url: str = ""
    events: List[EventsModel] = []
    recurring_batch_id: str = ""
    start_time: int = 0
    end_time: int = 0
    run_time: int = 0
    recording_time: int = 0
    streaming_time: int = 0
    start_by: MeetingSourceModel = None
    end_by: MeetingSourceModel = None
    cumulative_participant_time: int = 0
    scheduled_time: int = 0
    meeting_status: MeetingStatusEnum = MeetingStatusEnum.SCHEDULED
    participant_count: int = 0
    public_session_count: int = 0
    co_browsing_time: int = 0
    client_id: str
    co_browsings: List[CoBrowsingsModel] = []
    recordings: List[RecordingsModel] = []
    streamings: List[StreamingsModel] = []
    participant_durations: Dict[str, int] = {}
    created_on: int
    updated_on: int


class PaginatedMeetingsModel(PydanticBaseModel):
    records: List[MeetingsTableModel]
    count: int
