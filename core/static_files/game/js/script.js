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
        // If it's hard mode, highlight all valid moves and then declare the opposite player as winner
        if (selectedDifficulty === 'hard') {
            highlightAllValidMoves(); // Highlight all valid moves in green
            setTimeout(() => {
                declareWinner(currentPlayer === 'black' ? 'white' : 'black', 'Invalid move');
            }, 1000); // Show valid moves for 1 second before declaring the winner
        }
        return; // Invalid move, return early
    }

    board[row][col] = currentPlayer;
    moveCount++; // Increment move count
    moveCountElement.textContent = moveCount; // Update move count display
    flipPieces(row, col);
    switchPlayer();

    // Check if the game is over after the move
    checkGameOver(); // Check for win/lose/draw conditions
}

function highlightAllValidMoves() {
    const cells = boardElement.querySelectorAll('.cell');
    for (let row = 0; row < 8; row++) {
        for (let col = 0; col < 8; col++) {
            if (isValidMove(row, col, currentPlayer)) {
                const correctCell = cells[row * 8 + col]; // Get the correct cell in the grid
                correctCell.classList.add('correct-move'); // Add a green highlight
            }
        }
    }

    // Remove the highlight after 1 second
    setTimeout(() => {
        cells.forEach(cell => cell.classList.remove('correct-move'));
    }, 500);
}

// Add CSS for the highlighted correct move
const style = document.createElement('style');
style.innerHTML = `
    .correct-move {
        background-color: green !important;
    }
`;
document.head.appendChild(style);

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
        declareWinner(currentPlayer === 'black' ? 'white' : 'black', 'Timeout');
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

function declareWinner(winner, reason) {
    clearInterval(timerInterval);
    clearTimeout(moveTimeout);
    alert(`${winner.charAt(0).toUpperCase() + winner.slice(1)} Player Wins! Reason: ${reason}`);
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
        declareWinner('white', 'No valid moves for Black');
    } else if (!whiteHasMove) {
        declareWinner('black', 'No valid moves for White');
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
        selectedDifficulty = button.id; // Set selected difficulty
        resetGame(); // Restart game with new difficulty
    });
});

// Switch player function
function switchPlayer() {
    clearTimeout(moveTimeout); // Clear the previous timeout for the current player
    currentPlayer = currentPlayer === 'black' ? 'white' : 'black'; // Switch the current player
    clearInterval(timerInterval); // Stop the previous timer

    // Update the player piece display
    const playerPiece = document.getElementById('player-piece');
    playerPiece.className = `cell ${currentPlayer}`; // Change the class based on current player

    startTimer(); // Start the timer for the new current player
    renderBoard(); // Re-render the board to reflect the current player
}

// Handle difficulty button clicks
difficultyButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove the active class from all buttons
        difficultyButtons.forEach(btn => btn.classList.remove('active'));

        // Add the active class to the clicked button
        button.classList.add('active');

        selectedDifficulty = button.id; // Set selected difficulty
        resetGame(); // Restart game with new difficulty
    });
});
