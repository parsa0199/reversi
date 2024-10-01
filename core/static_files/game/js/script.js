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
let selectedDifficulty = null; // No difficulty selected initially
const difficultyTimeouts = {
    easy: 40,   // 40 seconds
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
    if (!isValidMove(row, col, currentPlayer)) {
        // If it's hard mode, highlight the correct moves before declaring the opposite player as winner
        if (selectedDifficulty === 'hard') {
            highlightValidMoves(currentPlayer === 'black' ? 'white' : 'black'); // Highlight valid moves for the opposite player
            setTimeout(() => {
                declareWinner(currentPlayer === 'black' ? 'white' : 'black');
            }, 500); // Delay for 2 seconds before declaring the winner
            return;
        }
        return; // Otherwise, just return for invalid move
    }

    board[row][col] = currentPlayer;
    moveCount++; // Increment move count
    moveCountElement.textContent = moveCount; // Update move count display
    flipPieces(row, col);
    switchPlayer();

    // Check if the game is over after the move
    checkGameOver(); // Check for win/lose/draw conditions
}

function highlightValidMoves(player) {
    const validMoves = [];
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (isValidMove(row, col, player)) {
                validMoves.push({ row, col });
            }
        }
    }

    validMoves.forEach(({ row, col }) => {
        const cell = boardElement.children[row * 8 + col];
        cell.classList.add('highlight'); // Add highlight class
    });

    // Remove highlights after 1 second
    setTimeout(() => {
        validMoves.forEach(({ row, col }) => {
            const cell = boardElement.children[row * 8 + col];
            cell.classList.remove('highlight'); // Remove highlight class
        });
    }, 1000);
}

function startTimer() {
    if (!selectedDifficulty) return; // Prevent starting timer if difficulty not selected

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

    if (selectedDifficulty) { // Only start timer if a difficulty is selected
        startTimer();
    }
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

function checkGameOver() {
    // Check if both players have valid moves
    const blackHasMove = hasValidMoves('black');
    const whiteHasMove = hasValidMoves('white');

    if (!blackHasMove && !whiteHasMove) {
        alert("It's a draw!");
        resetGame();
    } else if (!blackHasMove) {
        declareWinner('white');
    } else if (!whiteHasMove) {
        declareWinner('black');
    }
}

// Check if a player has any valid moves
function hasValidMoves(player) {
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (isValidMove(row, col, player)) {
                return true;
            }
        }
    }
    return false;
}

// Check if a move is valid
function isValidMove(row, col, player) {
    // Check if the cell is empty
    if (board[row][col]) return false;

    // Check all directions for valid flips
    const directions = [
        [-1, 0], [1, 0], [0, -1], [0, 1],
        [-1, -1], [-1, 1], [1, -1], [1, 1],
    ];

    for (const [dx, dy] of directions) {
        if (canFlip(row, col, dx, dy, player)) return true;
    }

    return false;
}

// Check if a piece can be flipped in a given direction
function canFlip(row, col, dx, dy, player) {
    let x = row + dx;
    let y = col + dy;
    let foundOpponent = false;

    while (x >= 0 && x < 8 && y >= 0 && y < 8) {
        if (!board[x][y]) break; // Empty cell found
        if (board[x][y] === player) return foundOpponent; // Found the same player

        foundOpponent = true; // Found an opponent piece
        x += dx;
        y += dy;
    }

    return false; // No valid flip found
}

// Flip pieces in the specified direction
function flipPieces(row, col) {
    const directions = [
        [-1, 0], [1, 0], [0, -1], [0, 1],
        [-1, -1], [-1, 1], [1, -1], [1, 1],
    ];

    for (const [dx, dy] of directions) {
        if (canFlip(row, col, dx, dy, currentPlayer)) {
            flipDirection(row, col, dx, dy);
        }
    }
}

// Flip pieces in the specified direction
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
        selectedDifficulty = button.id; // Get the selected difficulty
        resetTimers(); // Reset timers when a difficulty is selected
        alert(`Difficulty set to ${selectedDifficulty.charAt(0).toUpperCase() + selectedDifficulty.slice(1)}`);
    });
});
