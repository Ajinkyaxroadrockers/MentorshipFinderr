const mentorData = document.getElementById("mentor-data");
const mentorList = document.getElementById("mentor-list");
const searchInput = document.getElementById("mentor-search");

const category = mentorData.dataset.category;
let allMentors = [];

async function fetchMentors() {
  mentorList.innerHTML = '<div class="loading-card">Loading mentors...</div>';

  try {
    const response = await fetch(`/api/mentors?category=${encodeURIComponent(category)}`);
    allMentors = await response.json();
    renderMentors(allMentors);
  } catch (error) {
    mentorList.innerHTML = '<div class="loading-card">Unable to load mentors right now.</div>';
  }
}

function renderMentors(mentors) {
  if (mentors.length === 0) {
    mentorList.innerHTML = `
      <div class="empty-state">
        <i class="bi bi-search"></i>
        <h2>No mentors found</h2>
        <p>Try another expertise keyword or check this category later.</p>
      </div>
    `;
    return;
  }

  mentorList.innerHTML = mentors.map((mentor) => `
    <article class="mentor-card">
      <img src="${mentor.photo_path}" alt="${mentor.mentor_name}">

      <div class="mentor-info">
        <span class="pill">${mentor.category}</span>
        <h2>${mentor.mentor_name}</h2>
        <p><strong>Branch:</strong> ${mentor.branch}</p>
        <p><strong>Year:</strong> ${mentor.year}</p>
        <p><strong>Expertise:</strong> ${mentor.expertise}</p>
        <p><strong>Email:</strong> ${mentor.email}</p>
        ${mentor.linkedin ? `<p><strong>LinkedIn:</strong> <a href="${mentor.linkedin}" target="_blank">${mentor.linkedin}</a></p>` : ""}
        <a class="primary-btn" href="mailto:${mentor.email}">Contact Mentor</a>
      </div>
    </article>
  `).join("");
}

searchInput.addEventListener("input", () => {
  const keyword = searchInput.value.trim().toLowerCase();

  const filteredMentors = allMentors.filter((mentor) =>
    mentor.expertise.toLowerCase().includes(keyword)
  );

  renderMentors(filteredMentors);
});

fetchMentors();
