import { useReactMediaRecorder } from "react-media-recorder";
import "./SoundRecorder.css";

const SoundRecorder = () => {
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ video: false });
  return (
    <div className="container">
      <div className="sound-record-div">
        <div className="d-flex justify-content-center">
          {/* {status} */}
          <div className="btn-group" role="group">
            <button
              type="button"
              className="btn btn-success"
              onClick={startRecording}
              disabled={status === "recording"}
            >
              🔴 Start Recording
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={stopRecording}
              disabled={status !== "recording"}
            >
              Stop Recording
            </button>
          </div>
          <audio src={mediaBlobUrl} controls />
        </div>
        {/* {status === "recording" && (
            <div className="spinner-grow   spinner-grow-sm" role="status"></div>
          ) */}
      </div>
    </div>
  );
};

export default SoundRecorder;
