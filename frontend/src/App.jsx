import "./App.css";
import SudokuBoard from "./components/SudokuBoard";

function App() {
  return (
    <>
      <div className="min-h-screen bg-gray-100 py-8">
        <SudokuBoard />
      </div>
    </>
  );
}

export default App;
