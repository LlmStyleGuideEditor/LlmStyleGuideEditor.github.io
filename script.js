// Declare the textBoxes array globally
let textBoxes = [];

// Function to save data to localStorage
function saveData() {
  localStorage.setItem('textBoxes', JSON.stringify(textBoxes));
}

// Function to load data from localStorage
function loadData() {
  const storedData = localStorage.getItem('textBoxes');
  if (storedData) {
    textBoxes = JSON.parse(storedData);
    renderTextBoxes();
  }
}

// Function to add a resizable text box
function addResizableTextBox(section) {
  // Create elements
  const container = document.createElement("div");
  const textBox = document.createElement("textarea");
  textBox.setAttribute("rows", "4");
  textBox.setAttribute("cols", "50");
  container.appendChild(textBox);

  // Find the target section container
  const titleContainers = document.querySelectorAll('.title-container');
  for (let i = 0; i < titleContainers.length; i++) {
    if (titleContainers[i].textContent.includes(section)) {
      titleContainers[i].parentNode.insertBefore(container, titleContainers[i].nextSibling);
      break;
    }
  }

  // Push text box data to the array and save
  textBoxes.push({ section: section, value: textBox.value });
  saveData();
}

// Function to render text boxes from stored data
function renderTextBoxes() {
  textBoxes.forEach(textBoxData => {
    const container = document.createElement("div");
    const textBox = document.createElement("textarea");
    textBox.value = textBoxData.value;
    container.appendChild(textBox);
    // Assuming sections have unique IDs:
    document.getElementById(textBoxData.section.toLowerCase().replace(/ /g, '-')).parentNode.insertBefore(container, document.getElementById(textBoxData.section.toLowerCase().replace(/ /g, '-')).nextSibling);
  });
}

// Load data on page load
window.addEventListener('load', loadData);

// Attach event listeners to textareas for saving on change
const textAreas = document.querySelectorAll('textarea');
textAreas.forEach(textArea => {
  textArea.addEventListener('input', saveData);
});
