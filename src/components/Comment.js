// Comment.js
import React, { useState } from "react";

const Comment = ({ text }) => {
  const [isDone, setIsDone] = useState(false);

  const handleToggleDone = () => {
    setIsDone(!isDone);
  };

  return (
    <div>
      <input type="checkbox" checked={isDone} onChange={handleToggleDone} />
      <span style={{ textDecoration: isDone ? "line-through" : "none" }}>
        {text}
      </span>
    </div>
  );
};

export default Comment;
