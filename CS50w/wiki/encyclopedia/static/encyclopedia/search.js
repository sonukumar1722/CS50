// Real-time search filtering
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search');
    const entriesList = document.getElementById('entries-list');
    const entryItems = document.querySelectorAll('.entry-item');

    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();

            entryItems.forEach(item => {
                const text = item.textContent.toLowerCase();
                if (text.includes(query)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
});
