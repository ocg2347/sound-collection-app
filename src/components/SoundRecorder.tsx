import { useReactMediaRecorder } from "react-media-recorder";
import "./SoundRecorder.css";
import { useState } from "react";

interface Props {
  id: string;
  subject: string;
  taskDone: boolean;
  getTask: () => void;
  setTaskDone: (taskDone: boolean) => void;
}

const SoundRecorder = ({ id, subject, taskDone, getTask, setTaskDone }: Props) => {

  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ video: false });

  const [soundUploading, setSoundUploading] = useState<boolean>(false);
  const [uploadFailed, setUploadFailed] = useState<boolean>(false);

  const uploadSound = async () => {
    const formData = new FormData();
    formData.append("username", "dummy");
    formData.append("subject", subject);
    formData.append("id", id);
    // now save the blob to a local sound file
    await fetch(mediaBlobUrl!).then((res) => {
      return res.blob();
    }).then((blob) => {
      const file = new File([blob], id.concat(".wav"), { type: "audio/wav" });
      return file;
    }).then((file) => {
      formData.append("file", file);
    });

    await fetch(
      "/api/upload-sound",
      {
        method: "POST",
        body: formData,
      })
  }

  // wrap buttons and recorder in a column
  return (
    <div className="container">
      <div className="sound-record-div">
        <div className="d-flex justify-content-center">
          {/* {status}
          <ul>
            <li>status: {status}</li>
            <li>current subject: {subject}</li>
            <li>task id: {id}</li>
          </ul> */}
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
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                try {
                  setSoundUploading(true);
                  uploadSound();
                  setTaskDone(true);
                  setUploadFailed(false);
                }
                catch (e) {
                  setUploadFailed(true);
                  console.log(e);
                }
                finally {
                  setSoundUploading(false);
                }
              }}
              disabled={status !== "stopped" || soundUploading}
            >
              Upload
            </button>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => {
                setTaskDone(false);
                getTask();
              }}
              disabled={!taskDone}
            >
              Next Task
            </button>
          </div>
        </div>
        <div className="d-flex justify-content-center">
          <audio src={mediaBlobUrl!} controls />
        </div>

        {taskDone && <div className="alert alert-success" role="alert">
          Task done, you can continue to the next task.
        </div>}
        {uploadFailed && <div className="alert alert-dark" role="alert">
          Upload failed, please try again.
        </div>}
      </div>
    </div>
  );
};

export default SoundRecorder;
