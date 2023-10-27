document.addEventListener("DOMContentLoaded", function () {
    const showInstructionsButton = document.querySelector(".show-instructions");
    const instructions = document.querySelector(".how-to-use");
    const welcomeMessage = document.getElementById("welcomeMessage");
    const submitMessage = document.getElementById("submitMessage");
  
    if (showInstructionsButton && instructions) {
      showInstructionsButton.addEventListener("click", function () {
        if (instructions.classList.contains("hidden")) {
          instructions.classList.remove("hidden");
          instructions.classList.add("visible");
        } else {
          instructions.classList.remove("visible");
          instructions.classList.add("hidden");
        }
      });
    }
  
    if (welcomeMessage) {
      if (sessionStorage.getItem("welcomeShown")) {
        welcomeMessage.classList.remove("visible");
        welcomeMessage.classList.add("hidden");
      } else if (welcomeMessage.classList.contains("visible")) {
        setTimeout(() => {
          welcomeMessage.classList.remove("visible");
          welcomeMessage.classList.add("hidden");
        }, 5000);
        sessionStorage.setItem("welcomeShown", "true");
      }
    }
  
    if (submitMessage && submitMessage.classList.contains("visible")) {
      console.log("Attempting to hide submitMessage after 5 seconds.");
      setTimeout(() => {
        submitMessage.classList.remove("visible");
        submitMessage.classList.add("hidden");
      }, 5000);
    }
  });
  