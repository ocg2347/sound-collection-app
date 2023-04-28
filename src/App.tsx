import TextContainer from "./components/TextContainer";
import SoundRecorder from "./components/SoundRecorder";
import "./App.css";
import SignIn from "./components/SignIn";
import { useContext } from "react";
import AuthContext from "./contexts/AuthProvider";

function App() {
  const task = {
    id: "safddsfds",
    context: "this is a context",
    QAs: [
      {
        id: "asdsdf",
        question: "this is a question1",
        answer: "this is an answer1",
      },
      {
        id: "asdsdf2",
        question: "this is a question2",
        answer: "this is an answer2",
      },
      {
        id: "asdsdf3",
        question: "this is a question3",
        answer: "this is an answer3",
      },
      {
        id: "asdsdf4",
        question: "this is a question4",
        answer: "this is an answer4",
      },
      {
        id: "asdsdf5",
        question: "this is a question5",
        answer: "this is an answer5",
      },
    ],
  };
  // reach out to the auth context
  const { loggedIn, setLoggedIn } = useContext(AuthContext);
  // get the auth state and setter from the context:
  if (loggedIn !== true) {
    return <SignIn />;
  }

  return (
    <div>
      <nav className="navbar">
        <h5 style={{ marginLeft: "20px" }}>Sound Record App for Science 🚀</h5>
      </nav>
      <TextContainer task={task} />
      <SoundRecorder />
    </div>
  );
}

export default App;
