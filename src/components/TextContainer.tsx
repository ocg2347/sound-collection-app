import "./TextContainer.css";

interface TextProps {
  task: Task | undefined;
}

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

const TextContainer = ({ task }: TextProps) => {
  const text = task?.text;
  return (
    <div className="genel">
      <div className="text-container">
        <h5>Text</h5>
        <p>{text}</p>

      </div>
    </div>
  );
};

export default TextContainer;