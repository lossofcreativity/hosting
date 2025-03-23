const game = document.getElementById("game");
const bird = document.getElementById("bird");
const scoreDisplay = document.getElementById("score");

let birdTop = 200;
let birdVelocity = 0;
let gravity = 0.5;
let gameHeight = 600;
let gameWidth = 400;
let pipes = [];
let score = 0;
let gameOver = false;

// Bird movement
function updateBird() {
  birdVelocity += gravity;
  birdTop += birdVelocity;
  bird.style.top = birdTop + "px";

  // Check if bird hits the ground or ceiling
  if (birdTop > gameHeight - 30 || birdTop < 0) {
    endGame();
  }
}

// Create pipes
function createPipe() {
  const pipeGap = 150;
  const pipeHeight = Math.random() * (gameHeight - pipeGap - 100) + 50;

  const topPipe = document.createElement("div");
  topPipe.classList.add("pipe");
  topPipe.style.height = pipeHeight + "px";
  topPipe.style.top = "0";
  topPipe.style.left = gameWidth + "px";

  const bottomPipe = document.createElement("div");
  bottomPipe.classList.add("pipe");
  bottomPipe.style.height = gameHeight - pipeHeight - pipeGap + "px";
  bottomPipe.style.bottom = "0";
  bottomPipe.style.left = gameWidth + "px";

  game.appendChild(topPipe);
  game.appendChild(bottomPipe);

  pipes.push({ top: topPipe, bottom: bottomPipe });
}

// Move pipes
function movePipes() {
  pipes.forEach((pipe) => {
    const pipeLeft = parseFloat(pipe.top.style.left);
    pipe.top.style.left = pipeLeft - 2 + "px";
    pipe.bottom.style.left = pipeLeft - 2 + "px";

    // Check if pipe is off-screen
    if (pipeLeft < -70) {
      game.removeChild(pipe.top);
      game.removeChild(pipe.bottom);
      pipes.shift();
      score++;
      scoreDisplay.textContent = "Score: " + score;
    }

    // Check collision
    if (
      (pipeLeft < 90 && pipeLeft > 50) &&
      (birdTop < parseFloat(pipe.top.style.height) || birdTop > gameHeight - parseFloat(pipe.bottom.style.height))
    ) {
      endGame();
    }
  });
}

// End game
function endGame() {
  gameOver = true;
  alert("Game Over! Your score: " + score);
  window.location.reload();
}

// Game loop
function gameLoop() {
  if (!gameOver) {
    updateBird();
    movePipes();
    requestAnimationFrame(gameLoop);
  }
}

// Start game
document.addEventListener("keydown", () => {
  birdVelocity = -8; // Flap on spacebar press
});

setInterval(createPipe, 1500); // Create pipes every 1.5 seconds
gameLoop();