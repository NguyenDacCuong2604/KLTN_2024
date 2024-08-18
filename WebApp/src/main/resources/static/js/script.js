function toggleDropdown() {
    const dropdown = document.querySelector('.user-info .dropdown-menu');
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}
// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.closest('.user-info')) {
        const dropdowns = document.getElementsByClassName('dropdown-menu');
        for (let i = 0; i < dropdowns.length; i++) {
            const openDropdown = dropdowns[i];
            if (openDropdown.style.display === 'block') {
                openDropdown.style.display = 'none';
            }
        }
    }
}

