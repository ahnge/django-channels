var players = document.querySelector(".players");
var roomName = document.getElementById("game_board").getAttribute("room_name");
var char_choice = null;
var connectionString =
  "ws://" + window.location.host + "/ws/play/" + roomName + "/";
var gameSocket = new WebSocket(connectionString);
var gameBoard = [-1, -1, -1, -1, -1, -1, -1, -1, -1];
winIndices = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6],
];
let moveCount = 0;
let myturn = true;
let gameStarted = false;
const user = JSON.parse(document.getElementById("user").textContent);

let elementArray = document.getElementsByClassName("square");
for (var i = 0; i < elementArray.length; i++) {
  elementArray[i].addEventListener("click", (event) => {
    const index = event.target.dataset.index;
    console.log(gameStarted);
    if (gameBoard[index] == -1) {
      if (!myturn) {
        alert("Wait for other to place the move");
      } else if (!gameStarted) {
        alert("Wait for other player to join.");
      } else {
        myturn = false;
        document.getElementById("alert_move").style.display = "none"; // Hide
        make_move(index, char_choice);
      }
    }
  });
}

function make_move(index, player) {
  index = parseInt(index);
  let data = {
    event: "MOVE",
    message: {
      index: index,
      player: player,
    },
  };

  if (gameBoard[index] == -1) {
    moveCount++;
    if (player == "X") gameBoard[index] = 1;
    else if (player == "O") gameBoard[index] = 0;
    else {
      alert("Invalid character choice");
      return false;
    }
    gameSocket.send(JSON.stringify(data));
  }

  elementArray[index].innerHTML = player;
  const win = checkWinner();
  if (myturn) {
    if (win) {
      data = {
        event: "END",
        message: `${player} is a winner. Play again?`,
      };
      gameSocket.send(JSON.stringify(data));
    } else if (!win && moveCount == 9) {
      data = {
        event: "END",
        message: "It's a draw. Play again?",
      };
      gameSocket.send(JSON.stringify(data));
    }
  }
}

function reset() {
  gameBoard = [-1, -1, -1, -1, -1, -1, -1, -1, -1];
  moveCount = 0;
  myturn = true;
  document.getElementById("alert_move").style.display = "inline";
  for (var i = 0; i < elementArray.length; i++) {
    elementArray[i].innerHTML = "";
  }
}

const check = (winIndex) => {
  if (
    gameBoard[winIndex[0]] !== -1 &&
    gameBoard[winIndex[0]] === gameBoard[winIndex[1]] &&
    gameBoard[winIndex[0]] === gameBoard[winIndex[2]]
  )
    return true;
  return false;
};

function checkWinner() {
  let win = false;
  if (moveCount >= 5) {
    winIndices.forEach((w) => {
      if (check(w)) {
        win = true;
        windex = w;
      }
    });
  }
  return win;
}

const addPlayerToPlayerList = (user) => {
  players.innerHTML += `<h5>${user}</h5>`;
};

function connect() {
  gameSocket.onopen = function open() {
    console.log("WebSockets connection created.");
    gameSocket.send(
      JSON.stringify({
        event: "JOIN",
        message: { user },
      })
    );
  };

  gameSocket.onclose = function (e) {
    console.log(
      "Socket is closed. Reconnect will be attempted in 1 second.",
      e.reason
    );
    setTimeout(function () {
      connect();
    }, 1000);
  };
  // Sending the info about the room
  gameSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    let event = data["event"];
    let message = data["message"];
    switch (event) {
      case "START":
        reset();
        gameStarted = true;
        break;
      case "userList":
        players.innerHTML = "";
        for (let i = 0; i < message.users.length; i++) {
          addPlayerToPlayerList(message.users[i]);
        }
        break;
      case "userLeave":
        players.innerHTML = "";
        for (let i = 0; i < message.users.length; i++) {
          addPlayerToPlayerList(message.users[i]);
        }
        gameStarted = false;
        break;
      case "setCharChoice":
        char_choice = message.char_choice;
        break;
      case "JOIN":
        if (message.game_can_start) {
          gameSocket.send(
            JSON.stringify({
              event: "START",
              message: "",
            })
          );
        }
        players.innerHTML = "";
        for (let i = 0; i < message.users.length; i++) {
          addPlayerToPlayerList(message.users[i]);
        }
        break;
      case "END":
        alert(message);
        reset();
        break;
      case "MOVE":
        if (message["player"] != char_choice) {
          make_move(message["index"], message["player"]);
          myturn = true;
          document.getElementById("alert_move").style.display = "inline";
        }
        break;
      default:
        console.log("No event");
    }
  };

  if (gameSocket.readyState == WebSocket.OPEN) {
    gameSocket.onopen();
  }
}

connect();
