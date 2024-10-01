const boardElement = document.getElementById('board');
const currentPlayerElement = document.getElementById('current-player');
const restartButton = document.getElementById('restart');

let board = [];
let currentPlayer = 'black';

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
    if (!isValidMove(row, col)) return;

    board[row][col] = currentPlayer;
    flipPieces(row, col);
    currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
    renderBoard();
}

function isValidMove(row, col) {
    // Check if the cell is empty
    if (board[row][col]) return false;

    // Check all directions for valid flips
    const directions = [
        [-1, 0], [1, 0], [0, -1], [0, 1],
        [-1, -1], [-1, 1], [1, -1], [1, 1]
    ];

    for (const [dx, dy] of directions) {
        let x = row + dx;
        let y = col + dy;
        let hasOpponent = false;

        while (x >= 0 && x < 8 && y >= 0 && y < 8) {
            if (!board[x][y]) break;
            if (board[x][y] !== currentPlayer) {
                hasOpponent = true;
            } else if (hasOpponent) {
                return true; // Valid move found
            } else {
                break;
            }
            x += dx;
            y += dy;
        }
    }
    return false;
}

function flipPieces(row, col) {
    const directions = [
        [-1, 0], [1, 0], [0, -1], [0, 1],
        [-1, -1], [-1, 1], [1, -1], [1, 1]
    ];

    for (const [dx, dy] of directions) {
        let x = row + dx;
        let y = col + dy;
        let piecesToFlip = [];

        while (x >= 0 && x < 8 && y >= 0 && y < 8) {
            if (!board[x][y]) break;
            if (board[x][y] === currentPlayer) {
                for (const [fx, fy] of piecesToFlip) {
                    board[fx][fy] = currentPlayer; // Flip the pieces
                }
                break;
            } else {
                piecesToFlip.push([x, y]);
            }
            x += dx;
            y += dy;
        }
    }
}

restartButton.addEventListener('click', initializeBoard);

// Initialize the game on load
initializeBoard();
