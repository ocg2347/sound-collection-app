import TextContainer from "./components/TextContainer";
import SoundRecorder from "./components/SoundRecorder";
import 'bootstrap/dist/css/bootstrap.min.css';
import "./App.css";
import SignIn from "./components/SignIn";
import { useContext, useEffect, useState } from "react";
import AuthContext from "./contexts/AuthProvider";

interface Task {
  id: string;
  text: string;
  type: string;
  subject: string;
  paragraph: number;
  totalParagraphs: number;
  question: number;
  totalQuestions: number;
}

function App() {

  // reach out to the auth context
  const { loggedIn, userName } = useContext(AuthContext);
  // get the auth state and setter from the context:
  if (loggedIn !== true) {
    return <SignIn />;
  }
  // function which gets task from the server

  const [task, setTask] = useState<Task>();
  const [taskDownloading, setTaskDownloading] = useState<boolean>(false);
  const [taskDone, setTaskDone] = useState<boolean>(false);
  const [message, setMessage] = useState<string>("");

  const getTask = async () => {
    setTaskDownloading(true);
    await fetch(
      "/api/get-task", {
      method: "POST",
      body: JSON.stringify({ username: userName }),
      headers: {
        "Content-Type": "application/json",
      },
    }
    ).then((res) => {
      return res.json();
    }
    ).then((data) => {
      // if data contains message property, it means that the task is done
      if (data.message) {
        setMessage(data.message);
        console.log(data);
      }
      else{
        setTask(data);
      }
      setTaskDownloading(false);
    }
    );
  };

  // run getTask when the component loads
  useEffect(() => {
    getTask();
  }, []);

  return (
    <div>
      <nav className="navbar">
        <h5 style={{ marginLeft: "20px", marginBottom: "5px", marginTop:"5px"}}>Sound Record App for Science 🚀</h5>
      </nav>
      {(taskDownloading || (task === undefined))  ? <div className="spinner-grow   spinner-grow-sm" role="status"></div> :
        // now if the task does not compy with the interface, it will not be rendered:
        <>
          <TextContainer
            task={task}
          />
          <SoundRecorder
            id={task.id}
            subject={task.subject}
            getTask={getTask}
            taskDone={taskDone}
            setTaskDone={setTaskDone}
          />
        </>
      }
      {message === "" ? null :
        <div className="alert alert-success" role="alert">
          {message}
        </div>
      }

    </div>
  );
}

export default App;
