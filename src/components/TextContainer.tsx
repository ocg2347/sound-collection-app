import "./TextContainer.css";
import { useState } from "react";
import { ArrowRight, ArrowLeft } from "react-bootstrap-icons";

// import { ReactNode } from "react";

interface Props {
  task: task;
  // children: ReactNode;
}
interface task {
  id: string;
  context: string;
  QAs: QA[];
}
interface QA {
  id: string;
  question: string;
  answer: string;
}

const TextContainer = ({ task }: Props) => {
  const context = task.context;
  const QAs = task.QAs;
  const nQuestions = QAs.length;
  const [qIdx, setQIdx] = useState(0);

  return (
    <div className="genel">
      <div className="text-container">
        <h5>Context</h5>
        <p>{context}</p>
        <h5>
          Question {qIdx + 1} of {nQuestions}
        </h5>
        <p>{QAs[qIdx].question}</p>
        <div className="btn-group" role="group">
          <button
            type="button"
            className="btn btn-secondary"
            disabled={qIdx < 1}
            onClick={() => {
              setQIdx(qIdx - 1);
            }}
          >
            <ArrowLeft />
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            disabled={qIdx > nQuestions - 2}
            onClick={() => {
              setQIdx(qIdx + 1);
            }}
          >
            <ArrowRight />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TextContainer;
