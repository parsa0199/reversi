// Function to toggle the appearance of the resend link
function toggleResendLink(enabled) {
    var resendLink = document.getElementById('resendLink');
    if (enabled) {
        resendLink.classList.remove('disabled');
        resendLink.removeAttribute('aria-disabled');
        resendLink.href = '/accounts/verification/phone/send/'; // Update href attribute
    } else {
        resendLink.classList.add('disabled');
        resendLink.setAttribute('aria-disabled', 'true');
        resendLink.removeAttribute('href'); // Remove href attribute
    }
}

// Timer function to count down 60 seconds
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    var intervalId = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (timer <= 0) {
            clearInterval(intervalId); // Stop the timer
            toggleResendLink(true); // Enable the resend link
            display.style.display = 'none'; // Hide the timer display
        } else {
            timer--; // Decrement the timer if not zero
        }
    }, 1000);
}

window.onload = function () {
    var duration = 60; // 10 seconds for testing
    var display = document.getElementById('timer');
    var resendLink = document.getElementById('resendLink');
    
    startTimer(duration, display);
    toggleResendLink(false); // Initially disable the resend link
    resendLink.addEventListener('click', function(event) {
        if (resendLink.classList.contains('disabled')) {
            event.preventDefault();
        }
    });
};