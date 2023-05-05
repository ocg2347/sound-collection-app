import TextContainer from "./components/TextContainer";
import SoundRecorder from "./components/SoundRecorder";
import "./App.css";
import SignIn from "./components/SignIn";
import { useContext, useEffect, useState } from "react";
import AuthContext from "./contexts/AuthProvider";

interface Task {
  id: string;
  text: string;
  type: string;
  subject: string;
  paragraph: string;
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
      setTask(data);
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
        <h5 style={{ marginLeft: "20px" }}>Sound Record App for Science 🚀</h5>
      </nav>
      {(taskDownloading || (task === undefined)) ? <div className="spinner-grow   spinner-grow-sm" role="status"></div> :
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
    </div>
  );
}

export default App;
