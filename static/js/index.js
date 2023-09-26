console.log("Sanity check from index.js.");

// focus 'roomInput' when user opens the page
document.querySelector("#roomInput").focus();

// submit if the user presses the enter key
document.querySelector("#roomInput").onkeyup = function (e) {
  if (e.keyCode === 13) {
    // enter key
    document.querySelector("#roomConnect").click();
  }
};

// redirect to '/ttt/<roomInput>/'
document.querySelector("#roomConnect").onclick = function () {
  let roomName = document.querySelector("#roomInput").value;
  console.log(roomName);
  if (roomName.length > 0) {
    window.location.pathname = "ttt/" + roomName + "/";
  }
};
