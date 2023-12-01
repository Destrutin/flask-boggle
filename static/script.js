class Game {
  constructor(board) {
    this.board = board;
    this.score = 0;
    this.time = 60;
    this.timer = null;
    this.playCount = 0;
    this.highScore = 0;
    this.usedWords = new Set();
  }
  async startTime() {
    this.timer = setInterval(() => {
      this.time--;
      $(".timer").text(`Time Remaining: ${this.time}`);

      if (this.time <= 0) {
        this.endGame();
      }
    }, 1000);
  }

  endGame() {
    clearInterval(this.timer);
    $(".guess").prop("disabled", true);
    $(".message").text("Game Over");
    this.sendStats();
  }

  async sendStats() {
    const response = await axios.post("/update-stats", {
      score: this.score,
      highScore: this.highScore,
      playCount: ++this.playCount,
      // Use pre-increment here so the value is able to be sent with the AJAX request. (Used immediately rather than need to use a variable to store the post-increment value then return that.)
    });
  }

  async submit(evt) {
    evt.preventDefault();
    const $guess = $(".guess", this.board);
    let guess = $guess.val();

    if (this.usedWords.has(guess)) {
      $(".message").text(`${guess} has already been used`);
      $guess.val("");
      $guess.focus();
      return;
    }

    const response = await axios.get("/check-word", {
      params: { guess: guess },
    });
    const message = $(".message");

    if (response.data.result === "ok") {
      this.score += guess.length;
      $(".score").text(`Score: ${this.score}`);
      message.text(`Added: ${guess}`);
    } else if (response.data.result === "not-on-board") {
      message.text(`${guess} is not valid on the board`);
    } else if (response.data.result === "not-word") {
      message.text(`${guess} is an invalid word`);
    }

    $guess.val("");
    $guess.focus();
    $(".guess-form").submit(this.submit.bind(this));
  }
}
document.addEventListener("DOMContentLoaded", function () {
  const game = new Game(board);
  game.startTime();
});
