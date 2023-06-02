import "./TextContainer.css";
import ProgressBar from "react-bootstrap/ProgressBar";

interface TextProps {
  task: Task | undefined;
}

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

const TextContainer = ({ task }: TextProps) => {
  console.log(task);
  const text = task?.text;
  const paragraph = task?.paragraph! + 1;
  const totalParagraphs = task?.totalParagraphs;
  const question = task?.question! + 1;
  const totalQuestions = task?.totalQuestions;
  const progressParagraph = (paragraph / totalParagraphs!) * 100;
  // const progressQuestion = (question / totalQuestions!) * 100 / 2;
  const type = task?.type;
  var progressQuestion = 0;
  if (type === "question") {
    progressQuestion = ((2 * (question - 1)) / (totalQuestions! * 2)) * 100;
  } else {
    progressQuestion = (((2 * question) - 1) / (totalQuestions! * 2)) * 100;
  }
  // assume 5 QAs:
  // progress 0%: question=q1=> 2*0/10=0
  // progress 10%: question=a1=> 2*1-1/10=0.1
  // progress 15%: question=q2=> 2*1/10=0.2
  // progress 20%: question=a2=> 2*2-1/10=0.3
  return (
    <div className="genel">
      <div className="text-container">
        <p>Paragraph {paragraph} / {totalParagraphs}</p>
        <ProgressBar striped variant="success" now={progressParagraph} />
        <p>
          {type === "question" ? "Question" : null}
          {type === "answer" ? "Answer" : null}
          {"      "}
          {question} / {totalQuestions}
        </p>
        <p>
          {type === "context" ? "Context" : null}
        </p>

        <ProgressBar striped variant="success" now={progressQuestion} />
        <h5>Text</h5>
        <p>{text}</p>

      </div>
    </div>
  );
};

export default TextContainer;