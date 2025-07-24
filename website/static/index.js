function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);
    fetch(`/like-post/${postId}`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
    likeCount.innerHTML = data["likes"];
    if (data["liked"] === true) {
    likeButton.className = "fas fa-thumbs-up";
    } else {
    likeButton.className = "far fa-thumbs-up";
    }
    })
    .catch((e) => alert("Could not like post."));
    }

    setTimeout(() => {
    const alert = document.querySelector('.alert');
    if (alert) {
      alert.classList.remove('show');
    }
  }, 7000);

        const currentMonthYearEl = document.getElementById('currentMonthYear');
        const calendarGridEl = document.querySelector('.calendar-grid');
        const prevMonthBtn = document.getElementById('prevMonth');
        const nextMonthBtn = document.getElementById('nextMonth');

        let currentDate = new Date();
        let currentYear = currentDate.getFullYear();
        let currentMonth = currentDate.getMonth();

        /**
         * @param {number} month
         * @param {number} year
         */
        function renderCalendar(month, year) {
            while (calendarGridEl.children.length > 7) {
                calendarGridEl.removeChild(calendarGridEl.lastChild);
            }

            const monthNames = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ];
            currentMonthYearEl.textContent = `${monthNames[month]} ${year}`;

            const firstDayOfMonth = new Date(year, month, 1).getDay();

            const daysInMonth = new Date(year, month + 1, 0).getDate();

            const today = new Date();
            const todayDay = today.getDate();
            const todayMonth = today.getMonth();
            const todayYear = today.getFullYear();

            for (let i = 0; i < firstDayOfMonth; i++) {
                const emptyCell = document.createElement('div');
                emptyCell.classList.add('day-cell', 'empty');
                calendarGridEl.appendChild(emptyCell);
            }

            for (let day = 1; day <= daysInMonth; day++) {
                const dayCell = document.createElement('div');
                dayCell.classList.add('day-cell', 'rounded-3');
                dayCell.textContent = day;

                if (day === todayDay && month === todayMonth && year === todayYear) {
                    dayCell.classList.add('today');
                }

                dayCell.addEventListener('click', () => {
                    console.log(`Clicked on: ${monthNames[month]} ${day}, ${year}`);
                });

                calendarGridEl.appendChild(dayCell);
            }
        }

        function goToPrevMonth() {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            renderCalendar(currentMonth, currentYear);
        }

        function goToNextMonth() {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
            renderCalendar(currentMonth, currentYear);
        }

        prevMonthBtn.addEventListener('click', goToPrevMonth);
        nextMonthBtn.addEventListener('click', goToNextMonth);

        document.addEventListener('DOMContentLoaded', () => {
            renderCalendar(currentMonth, currentYear);
        });
