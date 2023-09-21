var closeMsgs = document.querySelectorAll(".close-msg");
closeMsgs.forEach((closeMsg) => {
  closeMsg.addEventListener("click", () => {
    closeMsg.remove();
  });
});
