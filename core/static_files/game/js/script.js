const boardElement = document.getElementById('board');
const currentPlayerElement = document.getElementById('current-player');
const blackTimeElement = document.getElementById('black-time');
const whiteTimeElement = document.getElementById('white-time');
const moveCountElement = document.getElementById('move-count');

let board = [];
let currentPlayer = 'black';
let blackTime = 0; // in seconds
let whiteTime = 0; // in seconds
let timerInterval;
let moveTimeout;
let moveCount = 0; // Counter for moves
const difficultyButtons = document.querySelectorAll('button[id]');
let selectedDifficulty = 'medium'; // Default difficulty
const difficultyTimeouts = {
    easy: 40,   // 20 seconds
    medium: 15, // 15 seconds
    hard: 10    // 10 seconds
};

function initializeBoard() {
    board = Array(8)
        .fill(null)
        .map(() => Array(8).fill(null));

    // Place initial pieces
    board[3][3] = 'white';
    board[3][4] = 'black';
    board[4][3] = 'black';
    board[4][4] = 'white';

    renderBoard();
    resetTimers();
}

function renderBoard() {
    boardElement.innerHTML = '';
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');

            if (board[row][col] === 'black') {
                cell.classList.add('black');
            } else if (board[row][col] === 'white') {
                cell.classList.add('white');
            }

            cell.addEventListener('click', () => handleCellClick(row, col));
            boardElement.appendChild(cell);
        }
    }
    currentPlayerElement.textContent = currentPlayer.charAt(0).toUpperCase() + currentPlayer.slice(1);
}

function handleCellClick(row, col) {
    if (!isValidMove(row, col)) {
        // If it's hard mode, declare the opposite player as winner immediately
        if (selectedDifficulty === 'hard') {
            declareWinner(currentPlayer === 'black' ? 'white' : 'black');
            return;
        }
        return; // Otherwise, just return for invalid move
    }

    board[row][col] = currentPlayer;
    moveCount++; // Increment move count
    moveCountElement.textContent = moveCount; // Update move count display
    flipPieces(row, col);
    switchPlayer();
}

function switchPlayer() {
    clearTimeout(moveTimeout); // Clear the previous timeout
    currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
    clearInterval(timerInterval);
    startTimer();
    renderBoard();
}

function startTimer() {
    const currentTimeElement = currentPlayer === 'black' ? blackTimeElement : whiteTimeElement;
    let timeCounter = currentPlayer === 'black' ? blackTime : whiteTime;

    timerInterval = setInterval(() => {
        timeCounter++;
        currentTimeElement.textContent = formatTime(timeCounter);

        if (currentPlayer === 'black') {
            blackTime = timeCounter;
        } else {
            whiteTime = timeCounter;
        }
    }, 1000);

    // Start move timeout based on selected difficulty
    moveTimeout = setTimeout(() => {
        declareWinner(currentPlayer === 'black' ? 'white' : 'black'); // Declare the opposite player as winner
    }, difficultyTimeouts[selectedDifficulty] * 1000); // Timeout based on selected difficulty
}

function resetTimers() {
    blackTime = 0;
    whiteTime = 0;
    blackTimeElement.textContent = '00:00';
    whiteTimeElement.textContent = '00:00';
    clearInterval(timerInterval);
    clearTimeout(moveTimeout);
    startTimer();
}

function formatTime(seconds) {
    const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
    const secs = String(seconds % 60).padStart(2, '0');
    return `${minutes}:${secs}`;
}

function declareWinner(winner) {
    clearInterval(timerInterval);
    clearTimeout(moveTimeout);
    alert(`${winner.charAt(0).toUpperCase() + winner.slice(1)} Player Wins!`);
    resetGame();
}

function resetGame() {
    moveCount = 0; // Reset move count
    moveCountElement.textContent = moveCount; // Update move count display
    initializeBoard();
}

function isValidMove(row, col) {
    // Check if the cell is empty
    if (board[row][col]) return false;

    // Check all directions for valid flips
    const directions = [
        [-1, 0], [1, 0], [0, -1], [0, 1],
        [-1, -1], [-1, 1], [1, -1], [1, 1],
    ];

    for (const [dx, dy] of directions) {
        if (canFlip(row, col, dx, dy)) return true;
    }

    return false;
}

function canFlip(row, col, dx, dy) {
    let x = row + dx;
    let y = col + dy;
    let foundOpponent = false;

    while (x >= 0 && x < 8 && y >= 0 && y < 8) {
        if (!board[x][y]) break; // Empty cell found
        if (board[x][y] === currentPlayer) return foundOpponent; // Found the same player

        foundOpponent = true; // Found an opponent piece
        x += dx;
        y += dy;
    }

    return false; // No valid flip found
}

function flipPieces(row, col) {
    const directions = [
        [-1, 0], [1, 0], [0, -1], [0, 1],
        [-1, -1], [-1, 1], [1, -1], [1, 1],
    ];

    for (const [dx, dy] of directions) {
        if (canFlip(row, col, dx, dy)) {
            flipDirection(row, col, dx, dy);
        }
    }
}

function flipDirection(row, col, dx, dy) {
    let x = row + dx;
    let y = col + dy;

    while (x >= 0 && x < 8 && y >= 0 && y < 8) {
        if (board[x][y] === currentPlayer) break; // Stop flipping when the same player's piece is found
        board[x][y] = currentPlayer; // Flip the piece
        x += dx;
        y += dy;
    }
}

// Initialize the board immediately on page load
initializeBoard();

// Handle difficulty button clicks
difficultyButtons.forEach(button => {
    button.addEventListener('click', () => {
        selectedDifficulty = button.id; // Set selected difficulty
        resetGame(); // Restart game with new difficulty
    });
});
