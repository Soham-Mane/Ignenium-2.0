import logo from "./logo.svg";
import "./App.css";
import StarRating from "./components/StarRating";
import CommentList from "./components/CommentList";

function App() {
  return (
    <div className="App">
      <h1>React Star Rating</h1>
      <StarRating totalStars={5} initialRating={3} />
      <CommentList />
    </div>
  );
}

export default App;
