import { useState, useEffect } from "react";

// Initial grid configuration
const initialGrid = [
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9],
];

const SudokuBoard = () => {
  const [grid, setGrid] = useState(initialGrid.map((row) => [...row]));
  const [isSolving, setIsSolving] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [ws, setWs] = useState(null);
  const [iterations, setIterations] = useState(0);
  const [conflicts, setConflicts] = useState(0);
  const [time, setTime] = useState(0);
  const [algorithm, setAlgorithm] = useState("");

  // Check if a cell is part of the initial puzzle
  const isFixedCell = (row, col) => initialGrid[row][col] !== 0;

  useEffect(() => {
    return () => {
      if (ws) ws.close();
    };
  }, [ws]);

  const handleCellChange = (row, col, value) => {
    if (isFixedCell(row, col)) return; // Prevent editing fixed cells

    const newValue =
      value === "" ? 0 : Math.max(0, Math.min(9, parseInt(value)));
    const newGrid = [...grid];
    newGrid[row][col] = newValue;
    setGrid(newGrid);
  };

  const solveSudoku = async () => {
    setIsSolving(true);
    setErrorMessage("");

    const socket = new WebSocket("ws://localhost:8000/ws/solve");
    setWs(socket);

    socket.onopen = () => {
      socket.send(
        JSON.stringify({
          grid: grid.map((row) => row.map((cell) => (isSolving ? cell : cell))),
        })
      );
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.error) {
        setErrorMessage(data.error);
        setIsSolving(false);
        return;
      }

      // Merge with initial grid to preserve fixed cells
      const mergedGrid = data.grid.map((row, i) =>
        row.map((cell, j) => (isFixedCell(i, j) ? initialGrid[i][j] : cell))
      );

      setGrid(mergedGrid);
      setIterations(data.iteration);
      setConflicts(data.conflicts);
      setAlgorithm(data.algorithm);
      setTime(data.time);
    };

    socket.onclose = () => setIsSolving(false);
    socket.onerror = () => setErrorMessage("Connection error");
  };

  const resetGrid = () => {
    setGrid(initialGrid.map((row) => [...row]));
    setIterations(0);
    setConflicts(0);
    setAlgorithm("");
    setTime(0);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6 text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Sudoku Solver</h1>
        <p className="text-gray-600">Using {algorithm} </p>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="grid grid-cols-9 gap-px bg-gray-200 mb-4">
          {grid.map((row, rowIndex) =>
            row.map((cell, colIndex) => (
              <div
                key={`${rowIndex}-${colIndex}`}
                className={`relative aspect-square m
                  ${
                    colIndex % 3 === 2 && colIndex !== 8
                      ? "border-r-2 border-gray-300"
                      : ""
                  }
                  ${
                    rowIndex % 3 === 2 && rowIndex !== 8
                      ? "border-b-2 border-gray-300"
                      : ""
                  }
                  ${colIndex === 0 ? "border-l-2 border-gray-300" : ""}
                  ${rowIndex === 0 ? "border-t-2 border-gray-300" : ""}
                  ${
                    isFixedCell(rowIndex, colIndex) ? "bg-gray-100" : "bg-white"
                  }
                `}
              >
                <input
                  type="number"
                  min="1"
                  max="9"
                  value={cell || ""}
                  onChange={(e) =>
                    handleCellChange(rowIndex, colIndex, e.target.value)
                  }
                  className={`w-full h-full text-center text-xl focus:outline-none ${
                    isFixedCell(rowIndex, colIndex)
                      ? "font-bold text-gray-700 cursor-not-allowed"
                      : "text-blue-600 focus:bg-blue-50"
                  }`}
                  disabled={isSolving || isFixedCell(rowIndex, colIndex)}
                />
              </div>
            ))
          )}
        </div>

        <div className="flex justify-center gap-4 mb-4">
          <button
            onClick={solveSudoku}
            disabled={isSolving}
            className={`px-6 py-2 rounded-lg font-medium ${
              isSolving
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-blue-600 hover:bg-blue-700 text-white"
            }`}
          >
            {isSolving ? "Solving..." : "Solve"}
          </button>

          <button
            onClick={resetGrid}
            className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Reset
          </button>
        </div>

        {errorMessage && (
          <div className="text-red-600 text-center mb-4">{errorMessage}</div>
        )}

        <div className="text-center text-gray-600">
          <p>Iterations: {iterations}</p>
          <p>Current Conflicts: {conflicts}</p>
          <p>Time : {time}</p>
        </div>
      </div>
    </div>
  );
};

export default SudokuBoard;
