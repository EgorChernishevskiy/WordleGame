import { RUWORDS } from './ruwords';

const WORD_LENGTH = 5;
const MAX_ATTEMPTS = 6;

let SECRET_WORD = getRandomWord();
let attempts = 0;

const gameBoard = document.getElementById("game-board") as HTMLElement;
const inputWord = document.getElementById("input-word") as HTMLInputElement;
const submitWordButton = document.getElementById("submit-word") as HTMLButtonElement;
const restartButton = document.getElementById("restart-game") as HTMLButtonElement;

function isValidWord(word: string): boolean {
    return RUWORDS.includes(word.toLowerCase());
}

function getRandomWord(): string {
    const randomIndex = Math.floor(Math.random() * RUWORDS.length);
    return RUWORDS[randomIndex];
}

function createGrid() {
    for (let i = 0; i < MAX_ATTEMPTS; i++) {
        for (let j = 0; j < WORD_LENGTH; j++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.setAttribute("id", `cell-${i}-${j}`);
            gameBoard.appendChild(cell);
        }
    }
    console.log("field created")
}

function checkWord(guess: string) {
    const result = Array(WORD_LENGTH).fill("absent");
    const secretWordArray = SECRET_WORD.split("");
    const usedLetters = Array(WORD_LENGTH).fill(false);

    for (let i = 0; i < WORD_LENGTH; i++) {
        if (guess[i] === SECRET_WORD[i]) {
            result[i] = "correct";
            usedLetters[i] = true;
        }
    }

    for (let i = 0; i < WORD_LENGTH; i++) {
        if (result[i] === "correct") continue;

        for (let j = 0; j < WORD_LENGTH; j++) {
            if (!usedLetters[j] && guess[i] === SECRET_WORD[j]) {
                result[i] = "present";
                usedLetters[j] = true;
                break;
            }
        }
    }

    return result;
}

function displayResult(guess: string, result: string[]) {
    for (let i = 0; i < WORD_LENGTH; i++) {
        const cell = document.getElementById(`cell-${attempts}-${i}`);
        if (cell) {
            cell.textContent = guess[i];
            cell.classList.add(result[i]);
        }
    }
}

submitWordButton.addEventListener("click", () => {
    const guess = inputWord.value.toLowerCase();

    if (guess.length !== WORD_LENGTH) {
        alert(`Word must be ${WORD_LENGTH} letters long.`);
        return;
    }

    if (!isValidWord(guess)) {
        alert("Invalid word! Please enter a valid word.");
        return;
    }

    const result = checkWord(guess);
    displayResult(guess, result);

    attempts++;

    if (guess === SECRET_WORD) {
        alert("Congratulations! You guessed the word.");
        return;
    }

    if (attempts === MAX_ATTEMPTS) {
        alert(`Game over! The word was ${SECRET_WORD}.`);
    }

    inputWord.value = "";
});

restartButton.addEventListener("click", () => {
    restartGame();
});

function restartGame() {
    attempts = 0;
    SECRET_WORD = getRandomWord();
    gameBoard.innerHTML = "";
    createGrid(); 
    inputWord.value = "";
    alert("Game restarted! Try to guess the new word.");
}

createGrid();