document.addEventListener('DOMContentLoaded', function () {
    var progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(function (bar) {
        var progress = bar.getAttribute('data-progress');
        bar.style.width = progress + '%';
    });
});
